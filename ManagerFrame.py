from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel

from Sample import *
from PIL import Image, ImageDraw

from Preset import *
from PresetSound import *
from PresetUI import *

import os
from os import listdir
from os.path import isfile, join

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

		self.waveform_bg_width = 640
		self.waveform_bg_height = 120

		self.waveform_image_pil = None

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
		percentage = (time / (sample.total_duration_ms))
		self.scaler.set(percentage*100.0)
		print("percentage: " + str(percentage) + " time: " + str(time) + " total_duration: " + str(sample.total_duration_ms))

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

			self.waveform_label = Label(self.waveformFrame, text="waveform")
			self.waveform_label.grid(row=0, column=0, sticky=N) 

			self.scaler = Scale(self.waveformFrame,fg="black", bg="black", bd=0, from_=0, to=100, orient=HORIZONTAL, length=640, showvalue=False, takefocus=False)
			self.scaler.grid(row=1, column=0, sticky=N)


		counter = 0
		for file in files:
			segments = file.split(".")

			if segments[0] in self.valid_names and (segments[1] == "wav" or segments[1] == "WAV"):

				sample = Sample(segments[0], file, self.sd_var.get(), self)
				if counter == 0:
					self.waveform_image_pil = PIL.Image.open(sample.get_waveform_path()).convert('RGB')
					self.waveform_image = PIL.ImageTk.PhotoImage(self.waveform_image_pil)
					self.waveform_label.configure(image=self.waveform_image)
					
				counter += 1
				self.samples[segments[0]] = sample




	def load_path(self):
		fname = askdirectory()
		self.sd_var.set(fname)


#if __name__ == "__main__":
#    MyFrame().mainloop()
