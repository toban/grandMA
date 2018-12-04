import bitarray

class Preset():

	variableDepth=[10,7,7,7, 7,8,10,10,8, 7,7]
	bitCoordinate=[0, 2, 1, 0, 7, 6, 6, 0, 2, 2, 1]

	RATE = 0 #//1024 - 10 R
	CRUSH = 1 #//127 - 7  C

	ATTACK = 2 #// 127 - 7        A
	RELEASE = 3 #// 127 - 7       R

	LOOP_LENGTH = 4 # // 127 - 7  L
	SHIFT_SPEED =  5 #  // 127 - 7 S

	START = 6 #//1024 - 10  S
	END = 7  #//1024 - 10   E

	SETTING = 8 #// 7 - 4  L

	#// = 29
	SAMPLE_NAME_1 = 9 #// 127 - 7
	SAMPLE_NAME_2 = 10 #// 127 - 7

	TUNED_BIT = 0 # //1
	LEGATO_BIT = 1 #//0
	REPEAT_BIT = 2 #//1
	SYNC_BIT = 3 #//1
	SHIFT_DIR_BIT = 4 #//0


	def __init__(self, path):

		self.name = path
		self.preset_bytes = []
		self.preset_bytes.append(bitarray.bitarray())
		self.preset_bytes.append(bitarray.bitarray())
		
		self.path = path
		
		with open(path, 'rb') as fh:
			self.preset_bytes[0].fromfile(fh, 12)
			self.preset_bytes[1].fromfile(fh, 12)

		self.preset_a = PresetSound(self.preset_bytes[0])
		self.preset_b = PresetSound(self.preset_bytes[1])


#preset1 = Preset("/media/toban/GRANDPA2/P0T.TXT")
#preset = Preset("/media/toban/GRANDPA2/P0S.TXT")


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
