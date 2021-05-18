import tkinter as tk
from typing import Container
from PIL import Image, ImageTk
import re
import constant
from functools import partial
from pynput.keyboard import Key, Controller
import time

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("640x480")
		self.master.maxsize(640,480)
		self.master.minsize(640,480)
		self.pack()
		self.create_widgets()
	def create_widgets(self):
		rowi = 0
		coli = 0
		
		for buttonStuff in buttonStuffs:
			buttonText = buttonStuff.button
			keys = buttonStuff.command
			photo = buttonStuff.photo 
			
			if photo == None:
				button = tk.Button(self, text=buttonText, command=partial(self.do_action, keys), height=constant.BTN_HEIGHT, width=constant.BTN_WIDTH)
			else:
				button = tk.Button(self, text=buttonText, image = photo, command=partial(self.do_action, keys))
			button.grid(row=rowi, column=coli)
			
			coli += 1
			
			if coli >= constant.MAX_COL_COUNT:
				coli = 0
				rowi += 1
		
	def do_action(self, keys):
		print("##################################")
		print("#        Starting Action         #")
		print("##################################")
		time.sleep(5)
		for key in keys:
			print("pressing " + key)
			#DEBUGGING CODE
			press_key(key)
		time.sleep(0.1)
		for key in keys:
			print("releasing " + key)
			#DEBUGGING CODE
			release_key(key)
		print("##################################")
		print("#        Action Complete         #")
		print("##################################")

class Command():
	def __init__(self, button, photoPath, command):
		self.button = button
		self.photoPath = photoPath
		if photoPath != '':
			image = Image.open(self.photoPath)
			image = image.resize((100, 100), Image.ANTIALIAS) # IDK if this is needed
			self.photo = ImageTk.PhotoImage(image)
		else:
			self.photo = None
		self.command = command

def press_key(key):
	if key == "SHIFT":
		keyboard.press(Key.shift)
	elif key == "L-SHIFT":
		keyboard.press(Key.shift_l)
	elif key == "R-SHIFT":
		keyboard.press(Key.shift_r)
	elif key == "CTRL":
		keyboard.press(Key.ctrl)
	elif key == "L-CTRL":
		keyboard.press(Key.ctrl_l)
	elif key == "R-CTRL":
		keyboard.press(Key.ctrl_r)
	elif key == "SPACE":
		keyboard.press(Key.space)
	elif key == "BACKSPACE":
		keyboard.press(Key.backspace)
	elif key == "{RELEASE}":
		# Then release all keys
		release_all_keys()
	elif key == "{PAUSE}":
		time.sleep(0.1)
	else:
		keyboard.press(key)
def release_key(key):
	if key == "SHIFT":
		keyboard.release(Key.shift)
	elif key == "L-SHIFT":
		keyboard.release(Key.shift_l)
	elif key == "R-SHIFT":
		keyboard.release(Key.shift_r)
	elif key == "CTRL":
		keyboard.release(Key.ctrl)
	elif key == "L-CTRL":
		keyboard.release(Key.ctrl_l)
	elif key == "R-CTRL":
		keyboard.release(Key.ctrl_r)
	elif key == "SPACE":
		keyboard.release(Key.space)
	elif key == "BACKSPACE":
		keyboard.release(Key.backspace)
	elif key == "{RELEASE}":
		# Then do nothing
		None
	elif key == "{PAUSE}":
		None
	else:
		keyboard.release(key)
def release_all_keys():
	for key in Key:
		keyboard.release(key)

# Start the App, this must be done early so we can create the image refrences
root = tk.Tk(className="Keyboard Test")
root.overrideredirect(True)
#root.attributes('-type', 'dock') #for linux?

keyboard = Controller() # DEBUGGING CODE


# Place to hold the button stuffs
buttonStuffs = []

# Loop through the TSV file
lines = open('buttonCommands.txt').readlines()
for line in lines:
	splitString = re.split(r'\t', line.rstrip('\n'))
	buttonText = splitString[constant.BTN_TEXT_COLUMN]
	photoPath = splitString[constant.BTN_IMAGE_COLUMN]
	command = re.split(',', splitString[constant.BTN_COMMAND_COLUMN])
	stuffToAdd = Command(buttonText, photoPath, command)
	buttonStuffs.append(stuffToAdd)

app = Application(master=root)
app.mainloop()