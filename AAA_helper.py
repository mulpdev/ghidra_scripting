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
        
    def getPointerAt(self, addr):
        #data = self.FPAPI.getDataAt(addr)
        #print(data)
        data = None
        if data:
            ptr = data.getValue()
        else:
            i = self.FPAPI.getInt(addr)
            h = self.signed_num_to_unsigned_hexstr(i)
            ptr = self.AF.getAddress(h)
        return ptr
        
    def signed_num_to_unsigned_hexstr(self, num):
        if num < 0:
            twosComp = self.twosCompliment(num)
            ret = hex(twosComp)[:-1] #strip off trailing L
            if ret[0] == '-': # remove negative sign
                ret = ret[1:]
            return ret
        else:
            return hex(num)
            
    def twosCompliment(self, num):
        # >>> hex(0x1234ABCD & (2**32-1))
        # '0x1234abcdL'
        
        if bits == 32:
            return (num ^ 0xFFFFFFFF) + 1
        elif bits == 64:
            return (num ^ 0xFFFFFFFFFFFFFFFF) + 1
        else
            raise ValueError("bits must be 32 or 64")
            
   def get_arbitrary_scalar_from_struct(self, addr, struct_member_dt, signed=False, big_endian=False):
	END = '<'
	if big_endian:
		END = '>'
		
	FMT = ['', 'B', 'H', '', 'I'] # unsigned
	if signed:
		for i in range(len(FMT)):
			try:
				FMT[i] = FMT[i].lower()
			except:
				pass

	length = struct_member_dt.getLength()
	try:
		data = getBytes(addr, length)
		try:
			fmtstr = '{}{}'.format(END, FMT[length])
			ret = struct.unpack(fmtstr, data)
		except IndexError as e:
			print("ERROR length: {}\ntype: {}\nstruct: {}".format(length, type(struct_member_dt), struct_member_dt))
	except MemoryAccessException:
		ret = ['BAD']
	return ret[0]
    
    # recursive but output is hacky and needs to be made recursively safe
    # print first of each depth, then all of same depth, then back 1? Use a dict maybe?
    
    WIDTH = 10
    PREFIX = '\s' * WIDTH
    SPACING = '\s' * 4
    output = ''
    def fake_struct_with_arbitrary_data(addr, struct_dt, depth):
        # global output   
        if depth == 0:
            output = ''
            output += "{} @ {}\n".format(struct_dt.getName(), addr)
        
        for comp in struct_dt.getComponents():
            cdt = comp.getDataType()
            line = "{} {}".format(SPACING * depth, cdt.getName())
            
            if isInstance(cdt, ghidra.program.database.StructureDB):
                output += "{:<{width}} {} {}\n".format('', SPACING*depth, cdt.getName(), width=WIDTH)
                if not fake_struct_with_arbitrary_data(addr, cdt, depth+1):
                    return None:
            else:
                value = None
                if isInstance(cdt, ghidra.program.database.ArrayDB) or \
                    isInstance(cdt, ghidra.program.database.CharDataType):
                        value = 'n/a'
                else:
                    signed = False
                    bigEnd = False
                    value = self.get_arbitrary_scalar_from_member(addr, cdt, signed, bigEnd)
                    if value != 'BAD':
                        if isInstance(cdt, ghidra.program.database.PointerDB):
                            tmp = AF.getAddress('0').add(value)
                            
                            #if not in_range(tmp):
                            #    # effectively if AddressViewSet.contains(addr)
                            #    pass
                            #    return None
        
        
                            value = "@ {}".format(tmp)
                            
                        else:
                            value = hex(value)
                    
                    field = comp.getFieldName()
                    if not field:
                        field = '':
                    line += ' {}'.format(field)
                    output += "{:<{width}} {}\n".format(value, linem width=WIDTH)
                addr = addr.add(cdt.getLength())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
