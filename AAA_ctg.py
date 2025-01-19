# Setup for pylance LSP
from ghidra import *
try:
    from ghidra.ghidra_builtins import *
    from ghidra.program.flatapi import * # should import flatapi stuff`
except:
    pass

import re
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

AF = currentProgram.getAddressFactory()
DTM = currentProgram.getDataTypeManager()
FM = currentProgram.getFunctionManager()
MEM = currentProgram.getMemory()
PL = currentProgram.getListing()
SM = currentProgram.getSymbolTable() # actually returns SymbolManager obj

def get_decomp_string(function):
    ifc = DecompInterface()
    ifc.openProgram(currentProgram)
    func_decomp = ifc.decompileFunction(function, 0, ConsoleTaskMonitor())
    ccode_markup = func_decomp.getCCodeMarkup()
    ctg = ccode_markup.getClangFunction()
    return ctg.toString()

def find_pattern_in_ctg(ctg, pattern):
    pattern = 'iVar1;'
    # for functions escape open paren to avoid 
    # "sre_constants.error: unbalanced parenthesis"
    #pattern = 'sigprocmask\('
    matches = [m.start() for m in re.finditer(pattern, ctg)]
    print(matches)



# main
faddr = currentAddress
function = FM.getFunctionContaining(faddr)
decompStr = get_decomp_string(function)
find_pattern_in_ctg(decompStr, '')
