from tkinter import *
from tkinter.filedialog import askopenfilename

import simpleaudio as sa
import subprocess
from os.path import isfile
import os
import PIL
from _thread import start_new_thread
import time
import librosa
from PIL import Image, ImageDraw
import numpy as np

def probe_file(filename):
	cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
	p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err =  p.communicate()
	return out

class OnsetDetector():

	def __init__(self, filename, durationMs=None):
		self.duration = durationMs / 1000
		self.filename = os.path.split(filename)[1]
		self.file_path = os.path.split(filename)[0]
		self.onsets = []

	def get_onset_path(self):
		return self.file_path + "/.grandMA/waveforms/" + self.filename + ".png" 

	def get_full_path(self):
		return self.file_path + "/" + self.filename

	def detect(self):
		onset_min_length = 2

		if self.onsets == []:
			self.load_file(self.get_full_path())
			#o_env = librosa.onset.onset_strength(self.data, sr=self.sampleRate)
			tempo, beats = librosa.beat.beat_track(y=self.data, sr=self.sampleRate, hop_length=512)
			#beat_times = librosa.frames_to_time(beats, sr=self.sampleRate, hop_length=512)
			#cqt = np.abs(librosa.cqt(self.data, sr=self.sampleRate, hop_length=512))
			#subseg = librosa.segment.subsegment(cqt, beats, n_segments=2)
			#subseg_t = librosa.frames_to_time(subseg, sr=self.sampleRate, hop_length=512)
			#times = librosa.times_like(o_env, sr=self.sampleRate)
			allOnsets = librosa.onset.onset_detect(y=self.data, sr=self.sampleRate, backtrack=True, units='time')
			last_onset_time = 0
			for onset in allOnsets:
				if((self.onsets == []) or (onset - last_onset_time > onset_min_length)):
					self.onsets.append(onset)
					last_onset_time = onset

				print(last_onset_time)

			print("tempo:" + str(tempo))
			print("beats:" + str(beats))
		return self.onsets

	def createImage(self):
		img = Image.new('RGBA', [640,120], (255, 0, 0, 0))
		data = img.load()

		positions = []
		for second in self.onsets:
			percentage = second / self.duration
			pos = int(percentage*img.size[0])
			positions.append(pos)
		print(positions)
		for x in range(img.size[0]):
			
			if(x in positions):
			    for y in range(img.size[1]):
			        data[x,y] = (
			            255,
			            255,
			            255
			        )
		img.save(self.get_onset_path())
		return img

	def load_file(self, filename):
		y, sr = librosa.load(filename)#, duration=self.duration)
		
		self.data = y
		self.sampleRate = sr

'''
		for x in range(img.size[0]):
		    for y in range(img.size[1]):
		        data[x,y] = (
		            x % 255,
		            y % 255,
		            (x**2-y**2) % 255,
		        )
'''