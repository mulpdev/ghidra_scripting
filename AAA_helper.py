class Helper
    '''
    This is a standalone python file and does not have access to FlatAPI from 
    the calling script. To fix, Helper is a class with a constructor
    that takes the FPAPI
    
        from ghidra.program.flatapi import FlatProgramAPI
        ...
        helper = Helper(FlatProgramAPI(currentProgram))
    '''
    def __init__(self, FPAPI):
        self.FPAPI = FPAPI
        self.AF = self.APAPI.getAddressFactory() # fails if bad FPAPI passed in
        
    def getPointer(self, addr, width_bytes=4):
        if width_bytes == 4:
            i = self.FPAPI.getInt(addr)
        else:
            i = self.FPAPI.getLong(addr)
        h = self.getUnsignedHexStr(i)
        ptr = self.AF.getAddress(h)
        return ptr
        
    def getUnsignedHexStr(self, num, width_bytes=4):
        if num < 0:
            twosComp = self.twosCompliment(num, width_bytes)
            ret = hex(twosComp)[:-1] #strip off trailing L
            if ret[0] == '-': # remove negative sign
                ret = ret[1:]
            return ret
        else:
            return hex(num)
            
    def twosCompliment(self, num, width_bytes):
        # >>> hex(0x1234ABCD & (2**32-1))
        # '0x1234abcdL'
        neg1 = 2**(width_bytes*8)
        return (num ^ neg1) + 1
        
    def getArbitraryValue(self, addr, dt, signed=False, big_endian=False):
        ENDIAN = '<'
        if big_endian:
            ENDIAN = '>'
            
        FORMAT = ['', 'B', 'H', '', 'I', '', '', '' , 'L'] # unsigned fmt

        length = dt.getLength()
        data = getBytes(addr, length) # can throw MemoryAccessException
        try:
            fmt = FORMAT[length]
            if signed:
                fmt = fmt.lower()
            fmtstr = '{}{}'.format(ENDIAN, fmt)
            ret = struct.unpack(fmtstr, data)
        except IndexError as e:
            print("ERROR length: {}\ntype: {}\nstruct: {}".format(length, type(dt), dt))
    
        return ret[0]
    
    # recursive but output is hacky and needs to be made recursively safe
    # print first of each depth, then all of same depth, then back 1? Use a dict maybe?
    
    WIDTH = 10
    PREFIX = '\s' * WIDTH
    SPACING = '\s' * 4
    output = ''
    def fake_struct_with_arbitrary_data(addr, struct_dt, depth):
        output = ''
        #output += "{} @ {}\n".format(struct_dt.getName(), addr)
            
        for comp in struct_dt.getComponents():
            cdt = comp.getDataType()
            line = "{} {}".format(SPACING * depth, cdt.getName())
            
            if isInstance(cdt, ghidra.program.database.StructureDB):
                line += "{:<{width}} {} {}\n".format('', SPACING*depth, cdt.getName(), width=WIDTH)
                new_out = fake_struct_with_arbitrary_data(addr.add(comp.getOffset()), cdt, depth+1)
                line += new_out
            else:
                value = None
                if isInstance(cdt, ghidra.program.database.ArrayDB) or \
                    isInstance(cdt, ghidra.program.database.CharDataType):
                        value = 'n/a'
                else:
                    signed = False # TODO make dependant on data type
                    bigEnd = False # TODO make dependant on cpu type
                    value = self.getArbitraryValue(addr.add(comp.getOffset()), cdt, signed, bigEnd)
                    
                    if isInstance(cdt, ghidra.program.database.PointerDB):
                        tmp = AF.getAddress('0').add(value)
                        value = "@ {}".format(tmp)
                    else:
                        if signed:
                            s = hex(value)
                        else:
                            s = self.getUnsignedHexStr(value)
                    
                    field = comp.getFieldName()
                    if not field:
                        field = '':
                    line += ' {}'.format(field)
                    line += "{:<{width}} {}\n".format(value, linem width=WIDTH)
                addr = addr.add(cdt.getLength())
            output += line
        return output
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
