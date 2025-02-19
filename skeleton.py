# Skeleton Python Script
#@author mulpdev
#@category mulpdev
#@keybinding 
#@menupath 
#@toolbar 

''' Python Imports '''
from __future__ import print_function

''' Setup for pylance LSP '''
import ghidra

# will fail during Runtime but needed to import pyi
try:
    from ghidra.ghidra.ghidra_builtins import *
except:
    pass

''' Ghidra imports (if needed)'''
# Example: from ghidra.program.flatapi import *

''' Globals '''
AF = currentProgram.getAddressFactory()
DTM = currentProgram.getDataTypeManager()
FM = currentProgram.getFunctionManager()
MEM = currentProgram.getMemory()
PL = currentProgram.getListing()
SM = currentProgram.getSymbolTable() # actually returns "SymbolManager" obj

TOOL = state.getTool()
PROJECT = TOOL.getProject()
PM = PROJECT.getProjectManager()

'''
YOUR CODE HERE
'''

def main():
    yourCode()

if __name__ == "__main__":
    main()
