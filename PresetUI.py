from tkinter import *
import PIL

from Preset import *
from os import listdir
from os.path import isfile, join


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



