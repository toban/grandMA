from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import PIL

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showerror

import os
from os import listdir
from os.path import isfile, join

import simpleaudio as sa

from _thread import start_new_thread
import time

import json
import subprocess
import bitarray

from subprocess import call



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



def probe_file(filename):
	cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
	p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err =  p.communicate()
	return out




class Sample(Frame):

	def get_waveform_path(self):
		return self.file_path + "/.grandMA/waveforms/" + self.grandpa_name + ".pgm" 

	def get_full_path(self):
		return self.file_path + "/" + self.filename

	def monitor_playback(self):

		start = 0
		while self.play_obj != None and self.play_obj.is_playing():
			start += 10.0
			self.manager.update_playback(self, start)
			time.sleep(0.01)

		self.manager.update_playback(self, self.total_duration_ms)
		self.buttonPlay.configure(text="Play")


	def playback(self):

		if self.play_obj == None or self.play_obj != None and not self.play_obj.is_playing():
			sa.stop_all()
			start_new_thread(self.monitor_playback,())
			self.play_obj = self.wave_obj.play()
			print(self.play_obj)
			self.manager.show_waveform(self)
			self.buttonPlay.configure(text="[ Stop ]")

		elif self.play_obj != None and self.play_obj.is_playing():
			self.play_obj.stop()
			self.buttonPlay.configure(text="Play")


		#from multiprocessing.dummy import Pool as ThreadPool 
		#pool = ThreadPool(4) 

		# open the urls in their own threads
		# and return the results
		#results = pool.map(playsound, [path])
		#pool.close() 
		#pool.join()
		#play = playsound(path)
		#print(play)
		#play_thread = start_new_thread(playsound, (path,)) 
		#print(play_thread)

	#def toJSON(self):


	def load_wave_file(self):

		self.wave_obj = sa.WaveObject.from_wave_file(self.get_full_path())
		self.play_obj = None

		out = probe_file(self.get_full_path())
		#out = subprocess.check_output(["ffprobe", path])
		#print(out)
		#print("22050 Hz, 1 channels" in str(out))

		args = str(out).split("\\n")
		duration_segments = args[7].split('=')[1].split(":")

		hours_ms = float(duration_segments[0]) * 60 * 60 * 1000
		minutes_ms = float(duration_segments[1]) * 60 *  1000
		seconds_ms = float(duration_segments[2]) * 1000
		
		#print(hours_ms)
		#print(minutes_ms)
		#print(seconds_ms)

		self.total_duration_ms = hours_ms + minutes_ms + seconds_ms
		#print("total duration: " + str(self.total_duration_ms)) 

		self.duration.set(args[7].split('=')[1])
		self.is_mono = args[2].split('=')[1]

		#print(self.duration)
		#print(args)

	def __init__(self, labelText, origFilename, filePath, manager):
		Frame.__init__(self, manager.root)

		self.manager = manager
		self.grandpa_name = labelText

		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(5, weight=1)
		self.grid(sticky=W+E+N+S)

		self.label = Label(self, text=labelText)
		self.label.grid(row=1, column=0, sticky=W)

		self.duration = StringVar()
		self.filename_var = StringVar()

		self.file_path = filePath

		if origFilename != None:

			self.filename = labelText + ".wav"
			self.filename_var.set(origFilename)

			path = self.file_path + "/" +  origFilename

			self.load_wave_file()

			if(not isfile(self.get_waveform_path())):
				self.create_waveform_file()

			opendata = PIL.Image.open(self.get_waveform_path())
			self.waveform_image = PIL.ImageTk.PhotoImage(opendata)
			
		else:
			self.filename = None

		#duration = re.compile(r'Duration: (\d\d:\d\d:\d\d.\d\d)')
		#print(duration.findall(str(out)))

		#f = open(self.preset_path, 'r')
		#self.preset_bytes = (ord(b) for b in f.read())

		self.filename_label = Entry(self, textvariable=self.filename_var)
		self.filename_label.grid(row=1, column=1, sticky=W)

		self.duration_label = Entry(self, textvariable=self.duration)
		self.duration_label.grid(row=1, column=2, sticky=W)

		#self.scale = Scale(self.master, from_=0, to=200, orient=HORIZONTAL, width=10)
		#self.scale.grid(row=2, column=1)

		self.buttonBrowse = Button(self, text="Browse", command=self.load_file, width=4, height=1)
		self.buttonBrowse.grid(row=1, column=3, sticky=W)

		self.buttonPlay = Button(self, text="Play", command=self.playback, width=5, height=1)
		self.buttonPlay.grid(row=1, column=4, sticky=W)

		self.buttonDelete = Button(self, text="Delete", command=self.delete_file, width=3, height=1)
		self.buttonDelete.grid(row=1, column=5, sticky=W)

	def delete_file(self):
		self.manager.remove(self)

	def create_waveform_file(self):
		subprocess.check_output(["ffmpeg", "-i", self.get_full_path(), "-y", "-filter_complex", "showwavespic=s=640x120", "-frames:v",  "1", self.get_waveform_path()])
		opendata = PIL.Image.open(self.get_waveform_path())
		self.waveform_image = PIL.ImageTk.PhotoImage(opendata)


	def load_file(self):
		fname = askopenfilename()
		if fname:

			if self.filename is None:
				self.filename = self.grandpa_name + ".wav"
				self.filename_var.set(self.filename)
				self.last_sample_path = fname

			out = subprocess.check_output(["ffmpeg", "-i", fname, '-y', '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '22050', self.get_full_path()])

			print(out)
			self.load_wave_file()

			#stream = ffmpeg.input(fname + ' ffmpeg-acodec pcm_s16le -ac 1 -ar 16000')
			#stream = ffmpeg.output(stream, '/tmp/testwav.wav')
			#ffmpeg.run(stream)

class ManagerFrame(Frame):
	def __init__(self, master, sd_path):
		Frame.__init__(self, master)
		self.root = master
		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(1, weight=1)
		self.grid(sticky=W+E+N+S)

		self.valid_names = []
		self.last_sample_path = None

		start = 48
		for i in range(start,91):
			if(not (i >= start+10 and i <= start+17)):
				name = "P" + chr(i)
				self.valid_names.append(name)

		self.sd_var = StringVar()
		self.samples = {}
		self.sd_var.set(sd_path)

		self.grandmaPath = self.sd_var.get() + "/" + ".grandMA/"
		self.grandmaImagePath = self.sd_var.get() + "/" + ".grandMA/waveforms/"
		
		if not os.path.exists(self.grandmaPath):
			os.makedirs(self.grandmaPath)   
				
		if not os.path.exists(self.grandmaImagePath):
			os.makedirs(self.grandmaImagePath)

		self.filename_label = Entry(master, textvariable=self.sd_var, width=48)
		self.filename_label.grid(row=1, column=1, sticky=W)

		self.button_sd_path = Button(master, text="Select SD path", command=self.load_path, width=10, height=1)
		self.button_sd_path.grid(row=1, column=0, sticky=W)

		self.button_load = Button(master, text="load", command=self.load_samples, width=10, height=1)
		self.button_load.grid(row=1, column=2, sticky=W)

		if os.path.exists(self.grandmaPath):
			self.load_samples()



	def save(self):
		print("saving ...")
		#obj = open(self.grandmaPath+'database.json', 'wb')

		#data= {}
		#data["last_sample_path"] = self.last_sample_path
		
		#obj.write(json.dumps(data))
		#obj.close

	def get_files(self, mypath):
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		return onlyfiles

	def update_playback(self, sample, time):
		percentage = (time / (sample.total_duration_ms*1.0))
		#print(str(sample.grandpa_name) + " time: " + str(time) + " percentage: " + str(percentage))
		self.scaler.set(percentage*100.0)


	def show_waveform(self, sample):

		print(sample.get_waveform_path())

		self.waveform_label.configure(image=sample.waveform_image)

	def delete_all(self):
		for sample in self.samples:
			self.samples[sample].delete_file()

	def add_new_multi(self):
		files = askopenfilenames()
		print(files)

	def add_new(self):
		name = None

		for name in self.valid_names:
			if not name in self.samples:
				break

		self.samples[name] = Sample(name, None, self.sd_var.get(), self)
		print("add new " + name)
		self.samples[name].load_file()
		self.samples[name].create_waveform_file()

	def remove(self, sample):

		if askokcancel("Delete file", "Are you sure wou wanna delete this?"):
			try:
				os.remove(sample.get_full_path())
				os.remove(sample.get_waveform_path())
			except OSError:
				pass
			
			sample.grid_forget()
			the_actual_sample = self.samples[sample.grandpa_name]
			print(the_actual_sample)



	def load_samples(self):
		start = 48
		self.samples = {}

		files = self.get_files(self.sd_var.get())
		#print(self.valid_names)

		self.button_sd_path.grid_forget()
		self.filename_label.grid_forget()
		self.button_load.grid_forget()

		self.button_new = Button(self, text="+ add new", command=self.add_new, width=20, height=1)
		self.button_new.grid(row=3, column=0, sticky=W)

		self.button_new_multi = Button(self, text="+ add multiple", command=self.add_new_multi, width=20, height=1)
		self.button_new_multi.grid(row=3, column=1, sticky=W)

		self.button_delete_all = Button(self, text="delete all", command=self.delete_all, width=20, height=1)
		self.button_delete_all.grid(row=3, column=2, sticky=W)

		self.select_path = Button(self, text="select path", command=self.load_path, width=20, height=1)
		self.select_path.grid(row=3, column=3, sticky=W)

#		self.menu_variable = StringVar(self)
#		self.menu_variable.set("one") # default value

		#self.menu = OptionMenu(self, self.menu_variable, "one", "two", "three")
		#self.menu.grid(row=3, column=3, sticky=W)
		
		self.waveform_image = None

		#self.canvas = Canvas(self, width=640, height=120)

		if self.waveform_image == None:

			self.waveformFrame = Frame(self.master)
			self.waveformFrame.rowconfigure(1, weight=1)
			self.waveformFrame.columnconfigure(1, weight=1)
			self.waveformFrame.grid(sticky=W+E+N+S)

			#print(self.samples[segments[0]].get_waveform_path())


			#self.canvas.create_image(20,20, anchor=NW, image=self.waveform_image)

			self.waveform_label = Label(self.waveformFrame, text="ASDASFA")
			self.waveform_label.grid(row=0, column=0, sticky=N) 

			self.scaler = Scale(self.waveformFrame,fg="black", bg="black", bd=0, from_=0, to=100, orient=HORIZONTAL, length=640, showvalue=False, takefocus=False)
			self.scaler.grid(row=1, column=0, sticky=N)


		counter = 0
		for file in files:
			segments = file.split(".")

			if segments[0] in self.valid_names and (segments[1] == "wav" or segments[1] == "WAV"):

				sample = Sample(segments[0], file, self.sd_var.get(), self)
				if counter == 0:
					opendata = PIL.Image.open(sample.get_waveform_path())
					self.waveform_image = PIL.ImageTk.PhotoImage(opendata)
					self.waveform_label.configure(image=self.waveform_image)
				counter += 1
				self.samples[segments[0]] = sample




	def load_path(self):
		fname = askdirectory()
		self.sd_var.set(fname)


#if __name__ == "__main__":
#    MyFrame().mainloop()

def calculate(*args):
	try:
		print("calculate")
		value = float(feet.get())
		meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
	except ValueError:
		pass



class PresetFrame(Frame):

	def get_waveform_path(self):
		if(self.preset == None):
			print("No preset selected ...")
		else:
			print(chr(self.preset.sample_1))
			print(chr(self.preset.sample_2))  

	def __init__(self, master, manager):
		Frame.__init__(self, master)

		self.preset = None

		self.manager = manager
		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(1, weight=1)
		self.grid(sticky=W+E+N+S)

		self.rate_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Rate")
		self.rate_scale.grid(row=2, column=1, sticky=N)

		self.crush_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Crush")
		self.crush_scale.grid(row=2, column=2, sticky=N)

		self.attack_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Attack")
		self.attack_scale.grid(row=2, column=3, sticky=N)

		self.release_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Release")
		self.release_scale.grid(row=2, column=4, sticky=N)

		self.loop_length_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Loop length")
		self.loop_length_scale.grid(row=2, column=5, sticky=N)

		self.shift_speed_scale = Scale(self, bd=0, from_=127, to=0, orient=VERTICAL, showvalue=True, takefocus=False, label="Shift speed")
		self.shift_speed_scale.grid(row=2, column=6, sticky=N)

		## --column
		self.loop_checkbox_var = IntVar()
		self.loop_checkbox = Checkbutton(self, text="looper", variable=self.loop_checkbox_var)
		self.loop_checkbox.grid(row=2, column=7, sticky=N)

		self.tuned_checkbox_var = IntVar()
		self.tuned_checkbox = Checkbutton(self, text="tuned", variable=self.tuned_checkbox_var)
		self.tuned_checkbox.grid(row=2, column=7, sticky=E)

		self.sync_checkbox_var = IntVar()
		self.sync_checkbox = Checkbutton(self, text="sync", variable=self.sync_checkbox_var)
		self.sync_checkbox.grid(row=2, column=7, sticky=S)

		## column
		self.legato_checkbox_var = IntVar()
		self.legato_checkbox = Checkbutton(self, text="legato", variable=self.legato_checkbox_var)
		self.legato_checkbox.grid(row=2, column=8, sticky=N)

		self.shift_dir_checkbox_var = IntVar()
		self.shift_dir_checkbox = Checkbutton(self, text="shift dir", variable=self.shift_dir_checkbox_var)
		self.shift_dir_checkbox.grid(row=2, column=8, sticky=E)

		if self.get_waveform_path() is not None:
			self.load_image(self.get_waveform_path())
		else:
			self.waveform_image = None
		self.waveform_label = Label(self, text="PRESET", image=self.waveform_image)
		self.waveform_label.grid(row=1, column=1, sticky=W) 
	

	def load_image(self, path):
		opendata = PIL.Image.open(path)
		self.waveform_image = PIL.ImageTk.PhotoImage(opendata)



class PresetEditor(Frame):

	def get_presets(self, path):
		self.presets = []
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		for file in onlyfiles:
			if file.endswith('.TXT'):
				self.presets.append(Preset(path+"/"+file))
				
		return self.presets
			
	def onselect(self, evt):
		# Note here that Tkinter passes an event object to onselect()
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		print('You selected item %d: "%s"' % (index, value))

		self.preset_a.get_waveform_path()
		self.preset_b.get_waveform_path()

		for preset in self.presets:
			if preset.name == value:
				print("")
				print("###########################################")
				print("## PRESET A  ##############################")
				print("###########################################")
				print(preset.preset_a)
				self.preset_a.preset = preset.preset_a
				self.preset_a.rate_scale.set(preset.preset_a.rate)
				self.preset_a.crush_scale.set(preset.preset_a.crush)
				self.preset_a.attack_scale.set(preset.preset_a.attack)
				self.preset_a.release_scale.set(preset.preset_a.release)
				self.preset_a.loop_length_scale.set(preset.preset_a.loop_length)
				self.preset_a.shift_speed_scale.set(preset.preset_a.shift_speed)

				self.preset_a.loop_checkbox_var.set(preset.preset_a.repeat)
				self.preset_a.legato_checkbox_var.set(preset.preset_a.legato)
				self.preset_a.shift_dir_checkbox_var.set(preset.preset_a.shift_dir)
				self.preset_a.sync_checkbox_var.set(preset.preset_a.sync)
				self.preset_a.tuned_checkbox_var.set(preset.preset_a.tuned)


				print("###########################################")
				print("## PRESET B  ##############################")
				print("###########################################")
				print(preset.preset_b)

				self.preset_b.preset = preset.preset_b
				self.preset_b.rate_scale.set(preset.preset_b.rate)
				self.preset_b.crush_scale.set(preset.preset_b.crush)
				self.preset_b.attack_scale.set(preset.preset_b.attack)
				self.preset_b.release_scale.set(preset.preset_b.release)
				self.preset_b.loop_length_scale.set(preset.preset_b.loop_length)
				self.preset_b.shift_speed_scale.set(preset.preset_b.shift_speed)

				self.preset_b.loop_checkbox_var.set(preset.preset_b.repeat)
				self.preset_b.legato_checkbox_var.set(preset.preset_b.legato)
				self.preset_b.shift_dir_checkbox_var.set(preset.preset_b.shift_dir)
				self.preset_b.sync_checkbox_var.set(preset.preset_b.sync)
				self.preset_b.tuned_checkbox_var.set(preset.preset_b.tuned)
				#self.start_scale.set(preset.preset_a.start)
				#self.end_scale.set(preset.preset_a.end)
				break
	def __init__(self, master, preset_path, manager):
		Frame.__init__(self, master)

		self.manager = manager
		self.root = master
		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(1, weight=1)
		self.grid(sticky=W+E+N+S)

		self.preset_a = PresetFrame(self, manager)
		self.preset_b = PresetFrame(self, manager)

		self.listboxFrame = Frame(self)
		self.listboxFrame.rowconfigure(1, weight=1)
		self.listboxFrame.columnconfigure(1, weight=1)
		self.listboxFrame.grid(sticky=W+E+N+S)

		self.listbox = Listbox(self.listboxFrame, width=100)
		self.listbox.grid(row=0, column=1, sticky=S)
		self.listbox.bind('<<ListboxSelect>>', self.onselect)

		for item in self.get_presets(preset_path):
			self.listbox.insert(END, item.name)

		self.delete_button = Button(self.listboxFrame, text="Delete", command=lambda lb=self.listbox: self.listbox.delete(ANCHOR))
		self.delete_button.grid(row=4, column=1, sticky=N)




root = Tk()
root.title("GrandMA: GrandPA Manager")

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def on_closing():
	
	#if askokcancel("Quit", "Do you want to quit?"):
	manager.save()
	root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

nb = ttk.Notebook(root)
mainframe = ttk.Frame(nb, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

sd_var = askdirectory(initialdir="/media/")#"/media/toban/GRANDPA2"
manager = ManagerFrame(mainframe, sd_var)
editor = PresetEditor(nb, sd_var, manager)

nb.add(mainframe, text='Samples')
nb.add(editor, text='Presets')
nb.grid(column=0)

root.mainloop()
