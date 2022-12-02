import os
import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile

'''
	screens/main.py
'''

class Main(tk.Frame):
	''' main landing screen for loggr '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)
		
		# objects
		self.main       = tk.Frame(self)
		self.btn_bar    = tk.Frame(self.main)
		self.lbl_greet  = tk.Label(self.main,font=('Arial',24),text='Welcome \nto \nLogWriter!')
		self.btn_create = tk.Button(self.btn_bar,borderwidth=3,relief='ridge',font=10,text='Create New')
		self.btn_search = tk.Button(self.btn_bar,borderwidth=3,relief='ridge',font=10,text='Search Existing')

		# config
		self.btn_create.id = 'create'
		self.btn_search.id = 'search'

		# grid
		self.main.grid(row=0,column=0)
		self.lbl_greet.grid(row=0,column=0,pady=20)

	def reset(self):
		pass