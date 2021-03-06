#imports
import sys, os, _thread
sys.path.append(os.path.abspath("tools/"))
from tools.spider import Spider
from tools.notes import Notes
from tools.dns_zone_transfer import DNSAttacks
from xss_tester import xss_start
from tools.brute import *

import tkinter as tk
from tkinter import ttk
#create a window
class Window(tk.Tk):
	def __init__(self):
		##########################Window Settings##############################
		super(Window, self).__init__()
		self.title("Tool Box By Tasaddar")
		self.minsize(640, 400)
		##########################Functions##############################
		#Coming Soon
		def coming_soon():
			print("coming soon")
		#Spider
		def spider():
			_thread.start_new_thread(Spider.spiderinit, (url.get(), thread.get(), loop.get(), depth.get(),))
		#DNS Forward
		def dns_forward():
			_thread.start_new_thread(DNSAttacks.nslookup, (url.get(),))
		#XSS Tester
		def xss_tester():
			_thread.start_new_thread(xss_start, (url.get(), thread.get(),))
		#Notes
		def note():
			_thread.start_new_thread(Notes.notes_start, ())
		#BruteForcer_Subdomain
		def subdomain():
			_thread.start_new_thread(subBrute.Start, (url.get(), thread.get(),))
		#Quit
		def quit():
			_thread.exit()
			exit()
		##########################Labels##############################
      #URL Label
		self.label = tk.Label(self, text="Input URL or Domain then select attack: ")
		self.label.grid(column=0, row=0, sticky="e")
		#Thread Label
		self.label = tk.Label(self, text="Input Thread Count: ")
		self.label.grid(row=0, column=2, sticky="e")
		#Loop Label
		self.label = tk.Label(self, text="Input Looping Count: ")
		self.label.grid(row=1, column=2, sticky="e")
		#Depth Label
		self.label = tk.Label(self, text="Input Depth Count: ")
		self.label.grid(row=2, column=2, sticky="e")
		##########################Buttons##############################
		#Spider
		self.button = tk.Button(self, text="Spider", command=spider)
		self.button.grid(row=1, column=0, sticky="nsew")
		#DNS Forwarding
		self.button = tk.Button(self, text="DNS Forward", command=dns_forward)
		self.button.grid(row=2, column=0, sticky="nsew")
		#XSS Checker
		self.xss = tk.Button(self, text="XSS Checker", command=xss_tester)
		self.xss.grid(row=3, column=0, sticky="nsew")
		#Subdomain Brute
		self.subbr = tk.Button(self, text="Subdomain brute", command=subdomain)
		self.subbr.grid(row=4, column=0, sticky="nsew")
		#Notes
		self.note = tk.Button(self, text="Notes", command=note)
		self.note.grid(row=5, column=0, sticky="s")
		#Close Button
		self.quit = tk.Button(self, text="Cancel", command=quit)
		self.quit.grid(row=6, column=0, sticky="s")
		##########################Entries##############################
		#URL Input
		url = tk.Entry(self, width=50, borderwidth=5)
		url.grid(row=0, column=1)
		url.focus_set()
		#Thread Input
		thread = tk.Entry(self, width=5, borderwidth=5)
		thread.grid(row=0, column=3)
		thread.insert(0, 10)
		#Loop Count
		loop = tk.Entry(self, width=5, borderwidth=5)
		loop.grid(row=1, column=3)
		loop.insert(0, 3)
		#Depth Count
		depth = tk.Entry(self, width=5, borderwidth=5)
		depth.grid(row=2, column=3)
		depth.insert(0, 1)
#enter mainloop for window
window = Window()
window.mainloop()

