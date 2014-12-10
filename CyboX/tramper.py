
# tramper.py
# Relocates bytes of an API and creates a jump from those bytes to the original API affectively negating a hook.
# TODO !Recalculate Relocated Relative jmp and call addresses.
# public domain code.

from ctypes import *
from win32api import *
from pytcc import pytcc
from struct import pack, unpack
from win32gui import PyGetString, PySetMemory, PySetString
from win32con import MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE, PROCESS_ALL_ACCESS

from distorm import Decode
from patcher import OpenProcess, readMemory, writeMemory, allocate, transport


DEBUG = True
def DB (msg):
global DEBUG
if DEBUG: print (msg)









def tramper (apiaddress, hook_size, apiname=None, dllname="kernel32"):
"""tramper (apiaddress, hook_size, apiname=None, dllname="kernel32"):
Creates a duplicate API using the trampoline method and returns its address.
"""

if DEBUG: global hprocess, landing_offset, instructions, landing_address, tramp_memory, tramp_code, original_bytes

if not apiaddress:
dll = LoadLibrary (dllname)
apiaddress = GetProcAddress (dll, apiname)

landing_offset = 0
hprocess = OpenProcess ()
original_bytes = PyGetString (apiaddress, 300)

tramp_memory = allocate (len (original_bytes) + 50, hprocess)
print "Tramp memory: %s %s." % (tramp_memory, hex (tramp_memory))

instructions = Decode (apiaddress, original_bytes)
sizes = iter ([X[1] for X in instructions])


while landing_offset < hook_size:

landing_offset += sizes.next ()


landing_address = apiaddress + landing_offset

DB ("Landing offset : %s %s" % (landing_offset, hex (landing_offset)))
DB ("Landing address: %s %s" % (landing_address, hex (landing_address)))

distance = landing_address - (tramp_memory +landing_offset)
DB ("Distance: %s %s." % (distance, hex (distance)))

tramp_code = original_bytes [:landing_offset] # api start - past hook - to start of instruction
instructions = Decode (apiaddress, tramp_code)


boffset = 0
for offset, size, instruction, hexstr in instructions:

if filter (lambda x:x.lower() in instruction.lower(), ["call", "jmp"]):
raise "[not supported yet] Cannot relocate CALL/JMP Instructions. Address: %s"% (apiaddress + boffset)

boffset += size


#
# TODO !Recalculate Relocated Relative jmp and call addresses.
#


jump_code = '\xe9' + pack ("i", distance - 5) # bytes = jmp (distance - size of jump)
tramp_code += jump_code

# DEBUG
DB ("Tramp [size]: %s [bytes]; %s" % (len(tramp_code), (repr(tramp_code))))
DB ("Tramper api decode.")
if DEBUG: dprint (apiaddress, tramp_code)
# # # #

writeMemory (hprocess, tramp_memory, tramp_code)
CloseHandle (hprocess)

return tramp_memory








def dprint (a, c):
""" pretty print disassembled bytes. dprint (offset, bytes)."""

x = Decode (a, c)
print "[deci addr : hexi addr] [size] instruction\n"

for offset, size, instruction, hexstr in x:

print "[%s : %s] [%s] %s" % (a,hex (a), size, instruction)
a += size







if __name__ == "__main__":

# Test.

lib = LoadLibrary ("kernel32")
OpenProcessAddr = GetProcAddress (lib, "OpenProcess")
FreeLibrary (lib)


trampAddr = tramper (\

apiaddress=OpenProcessAddr, # (optional if apiname is defined) API address to duplicate.
hook_size=10, # size of our API jmp code. (minimum size of relocated API bytes)
apiname=None, # (optional)
dllname="kernel32") # (optional / defaults to kernel32)



# Prototype the OpenProcess trampoline.
duplicate_OpenProcess = WINFUNCTYPE (c_int, c_int, c_int, c_int) (trampAddr)

pid = GetCurrentProcessId ()

print "Calling duplicate OpenProcess with pid: %s" % pid
phandle = duplicate_OpenProcess (0x1f0fff, 0, pid)
print "Return value: %s." %phandle

if phandle: CloseHandle (phandle)
