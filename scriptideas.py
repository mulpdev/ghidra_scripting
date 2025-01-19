import ghidra
from ghidra.app.plugin.core.navigation.locationreference import ReferenceUtils # this is a plugin, NOT a built into Ghidra thing
from ghidra.util.datastruct import ListAccumulator

public static void findDataTypeReferences(Accumulator<LocationReference> accumulator,
			DataType dataType, Program program, boolean discoverTypes, TaskMonitor monitor)
			throws CancelledException {

