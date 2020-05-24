from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import PIL

from ManagerFrame import *
from Preset import *
from PresetSound import *
from PresetUI import *
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
from os import system
from platform import system as platform

# set up your Tk Frame and whatnot here...

def calculate(*args):
	try:
		print("calculate")
		value = float(feet.get())
		meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
	except ValueError:
		pass

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

root.update()

if platform() == 'Darwin':
	initialdir = "/Volumes/"
else:
	initialdir = "/media/"
	
sd_var = askdirectory(initialdir=initialdir)#"/media/toban/GRANDPA2"
manager = ManagerFrame(mainframe, sd_var)
editor = PresetEditor(nb, sd_var, manager)

nb.add(mainframe, text='Samples')
nb.add(editor, text='Presets')
nb.grid(column=0)

root.mainloop()
