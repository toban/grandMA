from tkinter import *
from tkinter.filedialog import askopenfilename

import simpleaudio as sa
import subprocess
from os.path import isfile
import PIL
from _thread import start_new_thread
import time

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
		
		self.manager.root.update()
		self.manager.update_playback(self, self.total_duration_ms)
		self.buttonPlay.configure(text="Play")


	def playback(self):

		if self.play_obj == None or self.play_obj != None and not self.play_obj.is_playing():
			sa.stop_all()
			start_new_thread(self.monitor_playback,())
			self.play_obj = self.wave_obj.play()
			print(self.play_obj)
			self.manager.show_waveform(self)
			self.manager.root.update()
			self.buttonPlay.configure(text="[ Stop ]")

		elif self.play_obj != None and self.play_obj.is_playing():
			self.play_obj.stop()
			self.manager.root.update()
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

		self.buttonBrowse = Button(self, text="Browse", command=self.load_file, width=5, height=1)
		self.buttonBrowse.grid(row=1, column=3, sticky=W)

		self.buttonPlay = Button(self, text="Play", command=self.playback, width=5, height=1)
		self.buttonPlay.grid(row=1, column=4, sticky=W)

		self.buttonDelete = Button(self, text="Delete", command=self.delete_file, width=4, height=1)
		self.buttonDelete.grid(row=1, column=5, sticky=W)

	def delete_file(self):
		self.manager.remove(self)

	def create_waveform_file(self):
		subprocess.check_output(["ffmpeg", "-i", self.get_full_path(), "-y", "-filter_complex", "showwavespic=s=640x120", "-frames:v",  "1", self.get_waveform_path()])
		opendata = PIL.Image.open(self.get_waveform_path())
		self.waveform_image = PIL.ImageTk.PhotoImage(opendata)


	def load_file(self):
		self.manager.root.update()
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
