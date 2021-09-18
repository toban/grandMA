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
class SampleUI(Frame):

	def get_waveform_path(self):
		return self.sample.file_path + "/.grandMA/waveforms/" + self.grandpa_name + ".png" 

	def get_full_path(self):
		return self.sample.get_full_path()

	def monitor_playback(self):
		print('start playing')
		current = 0
		now = 0
		last = int(round(time.time() * 1000))
		now = int(round(time.time() * 1000))

		while self.play_obj != None and self.play_obj.is_playing():

			current = last - now
			#print(current / self.sample.total_duration_ms )
			self.manager.update_playback(self.sample, current)
			#print('update')
			last = int(round(time.time() * 1000))
			time.sleep(0.05)

		
		print (current, self.sample.total_duration_ms)
		self.manager.root.update()
		#self.manager.update_playback(self, self.sample.total_duration_ms)
		self.buttonPlay.configure(text="Play")


	def playback(self):

		if self.play_obj == None or self.play_obj != None and not self.play_obj.is_playing():
			sa.stop_all()
			self.play_obj = self.sample.wave_obj.play()
			start_new_thread(self.monitor_playback, ())
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


	def __init__(self, labelText, origFilename, sample, manager):
		Frame.__init__(self, manager.root)

		self.manager = manager
		self.grandpa_name = labelText

		self.master.rowconfigure(1, weight=1)
		self.master.columnconfigure(5, weight=1)
		self.grid(sticky=W+E+N+S)

		self.label = Label(self, text=labelText)
		self.label.grid(row=1, column=0, sticky=W)

		self.play_obj = None

		self.duration = StringVar()
		self.filename_var = StringVar()

		self.sample = sample

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

		self.buttonDetect = Button(self, text="Detect onsets", command=self.detect_onsets, width=20, height=1)
		self.buttonDetect.grid(row=1, column=5, sticky=W)

		self.create_waveform_file()

	def detect_onsets(self):
		self.manager.show_waveform(self)
		self.manager.root.update()
		self.sample.detector.detect()
		img = self.sample.detector.createImage()
		base_image = PIL.Image.open(self.get_waveform_path())
		base_image.putalpha(255)
		img.putalpha(255)
		#base_image.paste(img, (0,0))
		img = PIL.Image.blend(img, base_image, alpha=0.5);
		self.manager.waveform_image = PIL.ImageTk.PhotoImage(img)
		self.manager.waveform_label.configure(image=self.manager.waveform_image)


	def delete_file(self):
		self.manager.remove(self)

	def create_waveform_file(self):
		if not isfile(self.get_waveform_path()):
			subprocess.check_output(["ffmpeg", "-i", self.get_full_path(), "-y", "-filter_complex", "showwavespic=s=640x120", "-frames:v",  "1", self.get_waveform_path()])
		opendata = PIL.Image.open(self.get_waveform_path())
		self.waveform_image = PIL.ImageTk.PhotoImage(opendata)

	def load_file(self):
		self.manager.root.update()
		fname = askopenfilename()
		if fname:

			if self.sample.filename is None:
				self.sample.filename = self.grandpa_name + ".wav"
				self.filename_var.set(self.filename)
				self.last_sample_path = fname

			out = subprocess.check_output(["ffmpeg", "-i", fname, '-y', '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '22050', self.get_full_path()])

			self.sample.load_wave_file(self.get_full_path())


			#stream = ffmpeg.input(fname + ' ffmpeg-acodec pcm_s16le -ac 1 -ar 16000')
			#stream = ffmpeg.output(stream, '/tmp/testwav.wav')
			#ffmpeg.run(stream)
