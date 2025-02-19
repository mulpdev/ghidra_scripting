# Mark functions with their cumulative cyclomatic complexity
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
OG_PROG =  getCurrentProgram()    # Save off original program reference
SRC_PROG = OG_PROG                # Change to make use of another program for globals
AF = SRC_PROG.getAddressFactory()
DTM = SRC_PROG.getDataTypeManager()
FM = SRC_PROG.getFunctionManager()
MEM = SRC_PROG.getMemory()
PL = SRC_PROG.getListing()
SM = SRC_PROG.getSymbolTable() # actually returns "SymbolManager" obj

TOOL = state.getTool()
PROJECT = TOOL.getProject()
PM = PROJECT.getProjectManager()

''' Multi Program Helper Functions '''
def getByName(name, iter_thing, thing, exactSearch):
    if exactSearch:
        q = [_ for _ in iter_thing if _.name == name]
    else:
        q = [_ for _ in iter_thing if name.lower() in str(_.name).lower()]
	
    if len(q) != 1:
		err = "Found {} {} named {}\n\t{}".format(len(a), thing, name, a)
		raise Exception()
	return actions[0]

def getActionByName(name, exactSearch=True):
	return getByName(name, tool.getAllActions().iterator(), "Actions", exactSearch)
	
def getPluginByName(name, exactSearch=True):
	return getByName(name, tool.getManagedPlugins().iterator(), "Plugins", exactSearch)

def doAction(name, context):
	action = getActionByName(name)
	action.actionPerformed(context)
	
def getListingContext():
	return tool.getComponentProvider('Listing').getActionContext(None)
	
def doListingAction(name):
	doAction(name, getListingContext())

def updateGlobals(newProgram):
    if not isinstance(newProgram, ghidra.program.database.ProgramDB):
        return
    
    global SRC_PROG, AF, DTM, FM, MEM, PL, SM
    SRC_PROG = newProgram
    AF = SRC_PROG.getAddressFactory()
    DTM = SRC_PROG.getDataTypeManager()
    FM = SRC_PROG.getFunctionManager()
    MEM = SRC_PROG.getMemory()
    PL = SRC_PROG.getListing()
    SM = SRC_PROG.getSymbolTable()

def closeProgramHelper(program, ignoreChanges):
    if program == OG_PROG:
        print("Refusing to close OG program {}", program)
        return
    else:
        PM.closeProgram(program, ignoreChanges)

def closeAllProgramsHelper(ignoreChanges):
    for prog in PM.getAllOpenPrograms():
        closeProgramHelper(prog, ignoreChanges)

# path = "/<folder>/<binary>""
def openNewProgramInProject(path):
    plugin = getPluginByName('ProgramManagerPlugin')
    newProgram = plugin.openProgram(path)
    updateGlobals(newProgram)

'''
YOUR CODE HERE
'''
def main():
    pass

if __name__ == "__main__":
    path = AskString("Path", "Enter path to program in current project to open. Ex: /<folder>/<binary>")
    openNewProgramInProject(path)
    main()
    closeAllProgramsHelper(True)