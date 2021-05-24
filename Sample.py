from tkinter import *

from tkinter.filedialog import askopenfilename
import simpleaudio as sa
import subprocess
from os.path import isfile
import PIL
from _thread import start_new_thread
import time
from tkinter.simpledialog import askstring
from freesound_api import *
from dotenv import load_dotenv
load_dotenv()

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
		import time
		
		start = 0
		while self.play_obj != None and self.play_obj.is_playing():
			millis = int(round(time.time() * 1000))
			self.manager.update_playback(self, start)
			time.sleep(0.01)
			millisAfter = int(round(time.time() * 1000))
			start += millisAfter - millis

		self.buttonPlay.configure(text="Play")


	def playback(self):

		if self.play_obj == None or self.play_obj != None and not self.play_obj.is_playing():
			sa.stop_all()
			self.play_obj = self.wave_obj.play()
			print(self.play_obj)
			self.manager.show_waveform(self)
			self.buttonPlay.configure(text="[ Stop ]")
			start_new_thread(self.monitor_playback,())

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

		self.waveform_image_pil = None

		if origFilename != None:

			self.filename = labelText + ".wav"
			self.filename_var.set(origFilename)

			path = self.file_path + "/" +  origFilename

			self.load_wave_file()

			if(not isfile(self.get_waveform_path())):
				self.create_waveform_file()

			opendata = PIL.Image.open(self.get_waveform_path()).convert('RGBA')
			self.waveform_image_pil = opendata
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

		self.buttonPlay = Button(self, text="Play", command=self.playback, width=3, height=1)
		self.buttonPlay.grid(row=1, column=3, sticky=W)

		self.buttonBrowse = Button(self, text="Browse", command=self.load_file, width=4, height=1)
		self.buttonBrowse.grid(row=1, column=4, sticky=W)

		self.buttonDelete = Button(self, text="Delete", command=self.delete_file, width=3, height=1)
		self.buttonDelete.grid(row=1, column=5, sticky=W)

		self.freeSoundButton = Button(self, text="Freesound", command=self.freesound_query, width=8, height=1)
		self.freeSoundButton.grid(row=1, column=6, sticky=W)

		self.prevFreeSound = Button(self, text="<", command=self.prev_freesound, width=1, height=1)
		self.nextFreeSound = Button(self, text=">", command=self.next_freesound, width=1, height=1)
		
		self.nextFreeSound.grid_forget()
		self.nextFreeSound.grid_forget()
		
		self.freeSoundResult = None
		self.freeSoundCount = 0
		self.freeSoundResultIndex = 0
		API_KEY = os.getenv('FREESOUND_API_KEY')
		ACCESS_TOKEN = os.getenv('FREESOUND_ACCESS_TOKEN')
		self.api = FreesoundAPI(API_KEY, ACCESS_TOKEN)

	def prev_freesound(self):
		self.select_freesound(self.freeSoundResultIndex-1)

	def next_freesound(self):
		self.select_freesound(self.freeSoundResultIndex+1)

	def select_freesound(self, index):
		counter = 0
		print("num items:" + str(len(self.freeSoundResult['results'])))
		print("loading: " + str(index))
		for i in self.freeSoundResult['results']:
			if counter != index:
				counter+=1
				continue

			print("downloading: " + str(counter))

			self.freeSoundResultIndex = index
			sound = self.api.get_sound(i['id']).json()
			self.freeSoundButton.configure(text="Downloading")
			filename = self.api.download_sound(sound, self.api.get_preview(sound))
			self.load_file(filename)
			self.create_waveform_file()
			break
		
		self.freeSoundButton.configure(text=str(self.freeSoundResultIndex + 1) + "/" + str(self.freeSoundCount))
		self.manager.show_waveform(self)


	def freesound_query(self):
		var = askstring("Freesound query", "")
		print(var)
		if not var:
			return

		json = self.api.get_audio(var).json()
		self.freeSoundResult = json
		self.freeSoundCount = len(self.freeSoundResult['results'])
		self.select_freesound(0)
		self.prevFreeSound.grid(row=1, column=7, sticky=W)
		self.nextFreeSound.grid(row=1, column=8, sticky=W)
		
		print(var)

	def delete_file(self):
		self.manager.remove(self)

	def create_waveform_file(self):
		subprocess.check_output(["ffmpeg", "-i", self.get_full_path(), "-y", "-filter_complex", "showwavespic=s=640x120", "-frames:v",  "1", self.get_waveform_path()])
		self.waveform_image_pil = PIL.Image.open(self.get_waveform_path()).convert('RGBA')
		self.waveform_image = PIL.ImageTk.PhotoImage(self.waveform_image_pil)


	def load_file(self, fname):
		if not fname:
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
