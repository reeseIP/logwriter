import os
import pathlib
import tkinter as tk
import validation
from db import sql as db
from screens import notes, create, search
from tkinter import *
'''
  appv5.py
'''

class Window(tk.Tk):
	''' main window '''

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)

		# config
		self.title('Log Writer')
		self.geometry('960x1050+0+0')

		# paths
		self.app_path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
		self.file_dir = list(self.app_path.rglob('db/files'))[0]
		self.db_path  = list(self.app_path.rglob('*db.db'))[0]
		self.db_conn  = db.ConnectDB(path=self.db_path)
		self.iconSearch = PhotoImage(file=self.app_path.joinpath(pathlib.Path('img\\search.png')))

		# screen controllers
		self.validation = validation.Validate(self)
		self.notes 	= notes.Notes(self)
		self.create = create.Create(self)
		self.search = search.Search(self)

		# nav bar
		self.nav   = tk.Frame(self,bg='gray',borderwidth=2,relief='groove')
		self.h_title = tk.Label(self,font=('Arial',14,'bold'),text='loggr v5.0')

		# nav buttons
		self.btn_bar = tk.Frame(self.nav)
		self.src_bar = tk.Frame(self.nav)

		# self.btn_bar
		self.btn_n = tk.Button(self.btn_bar,text='Notes')
		#self.btn_s = tk.Button(self.btn_bar,text='Search')
		self.btn_c = tk.Button(self.btn_bar,text='Create')

		# self.src_bar
		self.ent_src = tk.Entry(self.src_bar,borderwidth=2,relief='sunken')
		self.btn_src = tk.Button(self.src_bar,image=self.iconSearch)

		# config
		self.btn_n.id = 'notes'
		self.btn_src.id = 'search'
		self.btn_c.id = 'create'
		self.btn_n.bind('<Button-1>', self.get_screen)
		self.btn_c.bind('<Button-1>', self.get_screen)
		self.btn_src.bind('<Button-1>',self.get_screen)
		self.btn_n.configure(font=('Arial',12,'bold'),fg='black',bg='light gray',width=6,borderwidth=2,relief='groove')
		self.btn_c.configure(font=('Arial',12,'bold'),fg='black',bg='light gray',width=6,borderwidth=2,relief='groove')
		self.btn_bar.configure(bg='gray')
		self.src_bar.configure(bg='gray')
		# self.nav grid
		self.btn_bar.pack(side='left')
		self.src_bar.pack(side='right')

		# self.btn_bar grid
		self.btn_n.grid(row=0,column=0,padx=(4,2),pady=4)
		self.btn_c.grid(row=0,column=2,padx=2)

		# self.src_bar grid
		self.ent_src.grid(row=0,column=0)
		self.btn_src.grid(row=0,column=1)

		# main window placement
		self.h_title.pack(padx=5,pady=3,anchor='w')
		self.nav.pack(fill='x')
		self.notes.pack(fill='both',expand=True,pady=(10,0))

		# currently displayed screen
		self.screen_id = self.notes

	def get_screen(self,event):
		''' get screen based on nav button click '''
		self.screen_id.pack_forget()
		self.screen_id.reset()
		
		if event.widget.id == 'notes':
			self.notes.pack(fill='both',expand=True,pady=(10,0))
			self.screen_id = self.notes
		elif event.widget.id == 'create':
			self.create.pack(anchor='sw',pady=(10,0))
			self.screen_id = self.create
		elif event.widget.id == 'search':
			self.search.pack(anchor='sw',fill='both',expand=True,pady=(10,0))
			self.search.search_value = self.ent_src.get()
			self.search.query()
			self.screen_id = self.search

root = Window()
root.mainloop()
