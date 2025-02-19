
from __future__ import print_function

DTM = currentProgram.getDataTypeManager()

THING='membername'

def forceConvertToString(s1, s2, caseSensitive):
    str1 = str(s1)
    str2 = str(s2)

    if caseSensitive == False:
        str1 = str1.lower()
        str2 = str2.lower()
    
    return (str1, str2)

def isIn(s1, s2):
    str1, str2 = forceConvertToString()

def memberLine(cdt, fieldname, offset, comment):
    line = "+- {:>25}  {:<5} {:<14}  {:<20}".format()
    return line

def findMemberName(pattern)
    for dt in DTM.getAllDataTypes():
        if isinstance(dt, ghidra.program.database.data.StructureDB):
            if not dt.getComponents():
                continue

            structname = dt.getName()
            print(structname)

            for comp in dt.getComponents():
                # skip any components without defined field name
                if not comp.getFieldName():
                    continue
                
                fieldname = comp.getFieldName()
                
                # swap for better string match with casesensitivity?
                if pattern.lower() in fieldname.lower():
                    offset = comp.getOffset() # not in hex
                    cdt = comp.getDataType()
                    comment = comp.getComment()
                    
                    line = memberLine(cdt, fieldname, offset, comment)
                    print(line)

def printStruct(pattern):
    pass

def main():
    pattern = AskString("Pattern", "Pattern to search for")
    findMemberName(pattern)