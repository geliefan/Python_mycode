# patcher.py
# handles patching and unpatching of process memory.
# public domain code.


from ctypes import *
from win32api import *
from pytcc import pytcc
from struct import pack, unpack, calcsize
from win32gui import PyGetString, PySetMemory, PySetString
from win32con import MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE, PROCESS_ALL_ACCESS
from distorm import Decode

DEBUG = True
def DB (msg):
  global DEBUG
  if DEBUG: print (msg)

def OpenProcess (pid=GetCurrentProcessId()):
  """Opens a process by pid."""
  DB ("[openProcess] pid:%s."%pid)
  phandle = windll.kernel32.OpenProcess (PROCESS_ALL_ACCESS,False,pid )
  assert phandle, "Failed to open process!\n%s" % WinError (GetLastError ()) [1]
  return phandle

def readMemory (phandle, address, size):
  """readMemory (address, size, phandle):"""
  cbuffer = c_buffer (size)

  success = windll.kernel32.ReadProcessMemory (\
phandle,
address,
cbuffer,
size,
0 )
  assert success, "Failed to read memory!\n%s" % WinError (GetLastError()) [1]
  return cbuffer.raw

def writeMemory (phandle, address=None, data=None):
  """Writes data to memory and returns the address."""
  assert data
  size = len (data) if isinstance (data, str) else sizeof (data)
  cdata = c_buffer (data) if isinstance (data, str) else byref (data)


  if not address: address = allocate (size, phandle)

  success = windll.kernel32.WriteProcessMemory (\

  phandle,
  address,
  cdata,
  size,
  0 )

  assert success, "Failed to write process memory!\n%s" % WinError (GetLastError()) [1]
  DB ("[write memory] :%s OK." % address)

  return address

def allocate (size, phandle):
  """Allocates memory of size in phandle."""

  address = windll.kernel32.VirtualAllocEx (\

  phandle,
  0,
  size,
  MEM_RESERVE | MEM_COMMIT,
  PAGE_EXECUTE_READWRITE )

  assert address, "Failed to allocate memory!\n%s" % WinError(GetLastError()) [1]
  DB ("[memory allocation] :%s" % address)

  return address








def releaseMemory (address, size, phandle):
  """Releases memory by address."""

  return windll.kernel32.VirtualFreeEx (\

  phandle,
  address,
  size,
  MEM_RELEASE )

  assert success, "Failed to read process memory!\n%s" % WinError(GetLastError()) [1]

  return cbuffer.raw








def transport (data, phandle):

  size = len (data)
  memory = allocate (size, phandle)
  writeMemory (phandle, memory, data)
  return memory








def get_patch (destination, params_size=0):

  """mov eax, destination
  call eax
  retn params_size
  """

  if isinstance (destination, (int,long)): destination = pack ("i", destination)
  if isinstance (params_size, (int,long)): params_size = pack ("h", params_size)

  return '\xb8%s\xff\xd0\xc2%s' % (destination, params_size)








def get_cparams_size (cparams):

  if not cparams: return 0

  s = ''

  for param in cparams:
    s += "size += sizeof (%s);\n" % param
    c_code = """
    int getsize ()
    {
    int size = 0;
    %s
    return size;
    }""" % s

  #DB (c_code)
  ccompiler = pytcc ()
  ccompiler.compile (c_code)
  ccompiler.relocate ()
  getsize = ccompiler.get_function ("getsize")
  size = getsize ()
  # ccompiler.delete ()
  return size




def get_cparams_size_b (cparams):
  return sum (map (calcsize, [param._type_ for param in cparams]))


def find_good_spot_to_patch (apiaddress, needed_size, maxscan=4000):
  """find_good_spot_to_patch (apiaddress, needed_size, maxscan=4000):
  Searches the instructions inside an API for a good place to patch."""

  # DEBUG
  if DEBUG == 2:
    bytes = PyGetString (apiaddress, needed_size * 2)
    dprint (apiaddress, bytes)
    # # # #

  aoffset = 0
  found_space = 0
  position = apiaddress


  while found_space < needed_size:
    bytes = PyGetString (position, 24)
    # DB ("found_space: %s. aoffset: %s. apiaddress: %s." % (found_space, aoffset, hex(position)))
    # if does_code_end_function (bytes): raise "Function end found before enough space was found!"
    offset, size, instruction, hexstr = Decode (position, bytes) [0]

  if "ret" in instruction.lower (): raise "Function end found before enough space was found!"

  if not filter (lambda x:x.lower() in instruction.lower(), ["call", "jmp"]):
    found_space += size
  else:
    found_space = 0

  aoffset += size
  if aoffset >= maxscan: raise "Maxscan exceeded while searching for a good spot to patch!"
  position += size


  return apiaddress + (aoffset - found_space)








class patcher:

  source = None
  destination = None
  jmp_asm = None
  original_bytes = None
  params_size = 0
  pid = None
  phandle = None


  duplicate_api = None
  original_api = None




def __init__ (self,

  source=None,
  destination=None,
  params_size=0,
  pid=GetCurrentProcessId () ):


  self.set_pid (pid)
  self.set_source (source)
  self.set_destination (destination)
  self.set_params_size (params_size)




def set_pid (self, pid):

  self.close ()
  self.phandle = OpenProcess (pid)
  self.pid = pid

def set_source (self, source): self.source = source
def set_destination (self, destination): self.destination = destination
def set_params_size (self, size): self.params_size = size
def set_source_as_api (self, apiname, dllname="kernel32.dll", free=True):

  module = LoadLibrary (dllname)
  procedure = GetProcAddress (module, apiname)
  if free: FreeLibrary (module)
  assert procedure
  self.original_api = eval ("windll.%s.%s" % (dllname.strip(".dll"), apiname))

  self.source = find_good_spot_to_patch (procedure, len (get_patch (0, self.params_size)))
  if DEBUG: DB ("found good spot to patch: %s %s. Offset from original api address: %s." \
  %(self.source, hex (self.source), self.source - procedure))




def patch (self):

  assert all ((self.phandle, self.source, self.destination)), "Patch source or destination not set!"
  assert not self.original_bytes, "Already patched!"

  self.jmp_asm = get_patch (self.destination, self.params_size)
  jmp_asm_size = len (self.jmp_asm)

  self.original_bytes = PyGetString (self.source, jmp_asm_size)
  assert self.original_bytes, "Failed to capture original_bytes."



  writeMemory (\
  phandle=self.phandle,
  address=self.source,
  data=self.jmp_asm)


  msg = "[jmp_asm]:%s\n[jmp_asm_size]:%s\n[original_bytes]:%s\n" \
  % (repr (self.jmp_asm), jmp_asm_size, repr (self.original_bytes))
  DB (msg)




def unpatch (self):

  if not self.original_bytes: raise "Not patched!"
  assert all ((self.phandle, self.source, self.destination)), "Not initialized!"

  writeMemory (\

  phandle=self.phandle,
  address=self.source,
  data=self.original_bytes )

  self.original_bytes = None


def close (self):

  if self.phandle:
    windll.kernel32.CloseHandle (self.phandle)
    self.phandle = None


def release (self):
  if self.phandle and self.duplicate_api:
    releaseMemory (self.duplicate_api, 0, self.phandle)


def call_original_api (self, *args, **kwargs): return self.original_api (*args, **kwargs)


def call_duplicate_api (self, types, *args, **kwargs):

  return WINFUNCTYPE (c_void_p, types) (self.duplicate_api) (*args, **kwargs)


def __del__ (self):

  try:self.unpatch ()
  except:pass
  try:self.release ()
  except:pass
  try:self.close ()
  except:pass








def dprint (a, c):
  """Pretty prints disassembled bytes. dprint (offset, bytes)."""
  x = Decode (a, c)

  print "[deci addr : hexi addr] [size] instruction\n"

  for offset, size, instruction, hexstr in x:
    print "[%s : %s] [%s] %s" % (a,hex (a), size, instruction)
    a += size
  print
