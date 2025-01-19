# above here is the default gui script stuff

bad = []
def commit_params(func):
    listingContext = getListingContext()
    #guiAction = doAction('Commit Params/Return', listingContext) # incorrect context
    funcPlugin = getPluginByName('DecompilePlugin').tool

    DI = ghidra.app.decompiler.DecompInterface()
    DI.openProgram(currentProgram)
    TIMEOUT = 1000
    decomp = DI.decompileFunction(func, TIMEOUT, getMonitor())
    highfunc = decomp.getHighFunction()

    from ghidra.program.model.symbol import SourceType
    from ghidra.program.model.pcode.HighFunctionDBUtil import commitParamsToDatabase, ReturnCommitOption

    #cmd = commitParamsToDatabase(hf, True, ReturnCommitOption.COMMIT, SourceType.USER_DEFINED)
    #funcPlugin.execute(cmd, listingContext.getProgram())

    try:
        commitParamsToDatabase(hf, True, ReturnCommitOption.COMMIT, SourceType.ANALYSIS)
        sys.stdout.write('Done\n')
    except:
        bad.append(func)
        sys.stdout.write('FAILED\n') # Why not print? I forget

i = 0
fcnt = currentProgram.getFunctionManager().getFunctionCount()
funcs = currentProgram.getFunctionManager().getFunctions(currentAddress, True)
for func in funcs:
    sys.stdout.write("{: 4}/{: 4} Commiting Params/Return for {} ...".format(i, fcnt, func))
    commit_params(func)
    i += 1

print("bad funcs")
for b in bad:
    print(b)
