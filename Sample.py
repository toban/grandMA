from tkinter import *
from tkinter.filedialog import askopenfilename

import simpleaudio as sa
import subprocess
from os.path import isfile
import PIL
from _thread import start_new_thread
import time
from OnsetDetector import *

def probe_file(filename):
	cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
	p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err =  p.communicate()
	return out

def convertFile(filename):
	cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
	p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err =  p.communicate()
	return out

class Sample(Frame):

	def get_full_path(self):
		return self.file_path + "/" + self.filename


	def load_wave_file(self, fullpath):

		print(fullpath)
		out = probe_file(fullpath)
		
		args = str(out).split("\\n")
		duration_segments = args[7].split('=')[1].split(":")

		hours_ms = float(duration_segments[0]) * 60 * 60 * 1000
		minutes_ms = float(duration_segments[1]) * 60 *  1000
		seconds_ms = float(duration_segments[2]) * 1000

		self.total_duration_ms = hours_ms + minutes_ms + seconds_ms

		self.duration = args[7].split('=')[1]
		self.is_mono = args[2].split('=')[1]

		self.play_obj = None

		try: 
			self.wave_obj = sa.WaveObject.from_wave_file(fullpath)
		except:
			print('error')
			return

	def __init__(self, filename, filePath):

		self.duration = None
		self.filename_var = None

		self.filename = filename
		self.file_path = filePath
		self.detector = None
		if filename != None and filePath != None:
			self.load_wave_file(self.get_full_path())
			self.detector = OnsetDetector(self.get_full_path(), self.total_duration_ms)

			
		else:
			self.filename = None
