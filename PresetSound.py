class PresetSound():

	def set_setting(self):
		setting = self.read_variable(Preset.SETTING)
		setting_bytes = bytes(setting)

		setting = bitarray.bitarray()
		setting.frombytes(setting_bytes)

		self.repeat=setting[Preset.REPEAT_BIT]
		self.tuned=setting[Preset.TUNED_BIT]
		self.shift_dir=setting[Preset.SHIFT_DIR_BIT]
		self.sync=setting[Preset.SYNC_BIT]
		self.legato=setting[Preset.LEGATO_BIT]
		self.slave = False
		if not self.tuned: 
			self.legato=False;
		if self.slave and self.sync: 
			self.sync=True;
		else: 
			self.sync=False;


  
	def setVar(self, _VARIABLE, _value):

		byteShift=0
		_bitCoordinate = 0
		
		for i in range(0, Preset.variableDepth[_VARIABLE]):


			if((bitCoordinate[_VARIABLE]+i)>15):
				byteShift=2
				_bitCoordinate = i-(16-bitCoordinate[_VARIABLE])
			elif((bitCoordinate[_VARIABLE]+i)>7):
				byteShift=1
				_bitCoordinate = i-(8-bitCoordinate[_VARIABLE])
			else:
				_bitCoordinate=bitCoordinate[_VARIABLE]+i
				

			bitState=value[i]
			self.preset_bytes[bitCoordinate] = bitState;

	def read_variable(self, _VARIABLE):

		variableDepth = Preset.variableDepth
		bitCoordinate = Preset.bitCoordinate

		_value=  bitarray.bitarray(variableDepth[_VARIABLE], endian='little')
		_byteShift=0
		_bitCoordinate=0

		for i in range(0, variableDepth[_VARIABLE]):

			if((bitCoordinate[_VARIABLE]+i) > 15):
				byteShift=2
				_bitCoordinate = i-(16-bitCoordinate[_VARIABLE]);
			elif((bitCoordinate[_VARIABLE]+i) > 7):
				byteShift=1;
				_bitCoordinate = i-(8-bitCoordinate[_VARIABLE]) #bitCount;
			else:
				_bitCoordinate=bitCoordinate[_VARIABLE]+i

			#bitState = bit_read(self.preset_bytes[byteCoordinate[_VARIABLE]+byteShift], _bitCoordinate);

			bitState = self.preset_bytes[_bitCoordinate];

			_value[i] = bitState
			#bitWrite(_value,i,bitState);

		return _value

	def read_bits(self):
		self.rate = int.from_bytes(self.read_variable(Preset.RATE).tobytes(), byteorder='big', signed=False)
		self.crush = int.from_bytes(self.read_variable(Preset.CRUSH).tobytes(), byteorder='big', signed=False)
		self.attack = int.from_bytes(self.read_variable(Preset.ATTACK).tobytes(), byteorder='big', signed=False)
		self.release = int.from_bytes(self.read_variable(Preset.RELEASE).tobytes(), byteorder='big', signed=False)
		self.loop_length = int.from_bytes(self.read_variable(Preset.LOOP_LENGTH).tobytes(), byteorder='big', signed=False)
		self.shift_speed = int.from_bytes(self.read_variable(Preset.SHIFT_SPEED).tobytes(), byteorder='big', signed=False)
		self.start = int.from_bytes(self.read_variable(Preset.START).tobytes(), byteorder='big', signed=False)
		self.end = int.from_bytes(self.read_variable(Preset.END).tobytes(), byteorder='big', signed=False)
		self.sample_1 = int.from_bytes(self.read_variable(Preset.SAMPLE_NAME_1).tobytes(), byteorder='little')
		self.sample_2 = int.from_bytes(self.read_variable(Preset.SAMPLE_NAME_2).tobytes(), byteorder='little')

	def __init__(self, bits):

		self.preset_bytes = bits

		self.read_bits()
		self.set_setting()

		print(self)
		#cprint(chr(sample_name_2))

	def __repr__(self):
		sound = "<PresetSound rate:%s crush:%s attack:%s release:%s loop_length:%s shift_speed:%s start:%s end:%s sample_1:%s sample_2:%s>" % (self.rate, self.crush, self.attack, self.release, self.shift_speed, self.loop_length, self.start, self.end, self.sample_1, self.sample_2)
		setting = "<PresetSettings repeat:%s tuned:%s shift_dir:%s sync:%s legato:%s >" % (self.repeat, self.tuned, self.shift_dir, self.sync, self.legato)
		
		return sound+'\n\t'+setting
