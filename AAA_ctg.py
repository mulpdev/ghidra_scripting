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
from ghidra.program.model.symbol import SourceType

from ghidra.program.model.listing import ParameterImpl

AF = currentProgram.getAddressFactory()
DTM = currentProgram.getDataTypeManager()
FM = currentProgram.getFunctionManager()
MEM = currentProgram.getMemory()
PL = currentProgram.getListing()
SM = currentProgram.getSymbolTable() # actually returns SymbolManager obj

'''
Clang Token Group functions
''' 

def get_ctg(function)
    DCI = DecompInterface()
    DCI.openProgram(currentProgram)
    decomp_results = DCI.decompileFunction(function, 0, ConsoleTaskMonitor()) # getMonitor() ???
    ctg = decomp_results.getCCodeMarkup()
    return ctg

def get_matching_tokens(ctg, pattern, ignore=None)
    ret = []
    for ct in ctg:
        if ct == ignore:
            continue
        if pattern in ct.toString():
            ret.append(ct)
    
    return ret

'''
Decompilation string functions

Function call patterns should escape the open parenethesis (
'''
class Needle:
    def __init__(substr, idxS_full, idxE_full, start_pattern, end_pattern):
        self.s = substr_full
        self.start = idxS_full
        self.end = idxE_full

        self.start_pattern = start_pattern
        self.end_pattern = end_pattern
    
    def modStart():
        return self.start + len(start_pattern)
    
    def modEnd():
        return self.end - len(end_pattern)

    def modS():
        return self.s[self.modStart():self.modEnd]

def get_needle_from_decomp_str(decomp_str, start_pattern, end_pattern):
    idxS = decomp_str.find(start_pattern)
    if idxS == -1:
        return None

    from_start = decomp_str[idxS:]
    idxE = from_start.find(end_pattern) 
    if idxE == -1:
        return None

    # make absolute offset including pattern
    idxE += len(end_pattern)
    idxE += idxS

    substr = decomp_str[idxS:idxE]
    return Needle(substr, idxS, idxE, start_pattern, end_pattern)

def get_all_needles_from_decomp_str(decomp_str, start_pattern, end_pattern):
    idxS = 0
    ret = []
    while True:
        needle = get_needle_from_decomp_str(decomp_str[idxS:], start_pattern, end_pattern)
        if needle:
            ret.append(needle)
            idxS += needle.end + 1
        else:
            break

    return ret

def get_function_call_params_in_decomp_str(decomp_str, function_name)
    ret = []
    FUNC_CALL_START = '{}\('.format(function_name)
    FUNC_CALL_END = ');'
    needles = get_all_needles_from_decomp_str(decomp_str, FUNC_CALL_START, FUNC_CALL_END, include_pattern=False)
    for n in needles:
        call = n.modS()
        ret.appened(call.split(','))

def find_pattern_indicies_decomp(decomp_str, pattern):
    matching_indicies = [m.start() for m in re.finditer(pattern, decomp_str)]
    return matching_indicies

def update_decomp_variable_dt(func, pattern, newdt):
    hfDBUtil = ghidra.program.model.pcode.HighFunctionDBUtil
    ctg = get_ctg(func)
    
    pattern = 'some_struct_t *'
    tokens = get_matching_clang_tokens(ctg, pattern)
    for t in tokens:
        variable_name = t.toString()[len(pattern):] # only need the variable name, not the datatype
        hfDBUtil.updateDBVariable(t.highSymbol, variable_name, newdt, SourceType.USER_DEFINED)

def update_function_parameter(func, newdt):
    # where can be of type Address, Register, or a long indicating a stack offet
    #where = toAddr('1234ABCD')
    #where = currentProgram.getProgramContext().getRegisters()[0]
    where = 0 # stack offset
    
    param = ParameterImpl("variable_name", newdt, where, SourceType.USER_DEFINED)
    func.addLocalVariable(param, SourceType.USER_DEFINED)


addr = toAddr('0xDEADBEEF')
func = FM.getFunctionContaining(addr)
ctg = get_ctg(func)
decomp_str = ctg.getClangFunction()