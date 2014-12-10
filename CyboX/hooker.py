# hooker.py
# deals with hooking of win32 APIs.
# public domain code.


from patcher import *
from tramper import tramper
from win32api import *
from pytcc import pytcc







def create_hook (duplicate_api, cparam_types='', prelogic="", postlogic="", restype="int"):
""" create_hook (pat, duplicate_api, cparam_types='', prelogic="", postlogic="", restype="int"):
"""

c_code =\
"""
%s function (int caller, %s)
{
%s
%s RET = DUPE ( %s );
%s
return RET;
}"""

cargs = ''
symbols = ''
for arg, char in zip (cparam_types, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):

symbols += "%s, " % char
cargs += "%s %s, " % (arg, char)

symbols = symbols [:-2]
cargs = cargs [:-2]

c_code = c_code % (restype, cargs, prelogic, restype, symbols, postlogic)
ccompiler = pytcc ()
ccompiler.add_lib_proc ("msvcrt.dll", "memset")
ccompiler.add_symbol ("DUPE", duplicate_api)
ccompiler.compile (c_code)
ccompiler.relocate ()

hook = ccompiler.get_symbol ("function")

return (c_code, hook)








def hooker (apiname, cparam_types=list(), restype="int", prelogic='', postlogic='', pid=GetCurrentProcessId(), dllname="kernel32"):
"""hooker (apiname, cparam_types=list(), restype="int", prelogic='', postlogic='', pid=GetCurrentProcessId(), dllname="kernel32"):
"""

pat = patcher ()

params_size = get_cparams_size (cparam_types)
pat.set_params_size (params_size)

pat.set_source_as_api (apiname, dllname)

hook_size = len (get_patch (pat.destination, pat.params_size))
tramp = tramper (pat.source, hook_size)
pat.duplicate_api = tramp

hook_ccode, hooks = create_hook (tramp, cparam_types, prelogic, postlogic, restype)
pat.c_code = hook_ccode
pat.set_destination (hooks)

return pat








if __name__ == '__main__':

# Test.


hook = hooker (\

# API to hook
apiname="OpenProcess",

# the DLL the API is in. (defaults to kernel32)
dllname="kernel32",

# (required) API parameter types. In our hook these get translated to the names A,B,C...respectively.
cparam_types=["int", "int", "int"],

# (required) the API return type.
restype="int",

# (optional) this is the code in our hook wich is executed Before the real API.
prelogic="if (C==1) {return 1111;}",

# (optional) this is the code in our hook wich is executed After the real API. The real API's return value is named RET.
postlogic="if (RET) {return 0;}"
)


# hook API.
# hook automatically unhooks itself and cleans up when it isnt refered to anymore.
hook.patch ()

print "Calling hooked OpenProcess api with process id as 1."
ret = windll.kernel32.OpenProcess (0x1f0fff, 0, 1)

print "Return value: %s" % ret
if ret == 1111: print "This test was sucesful."
else: print "Return value is unexpected."

# unhook API.
# hook.unpatch ()



#cad
