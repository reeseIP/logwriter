import os
import pathlib
import tkinter as tk
import validation
from db import sql as db
from screens import main, create, search

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

		# screen controllers
		self.validation = validation.Validate(self)
		self.main 	= main.Main(self)
		self.create = create.Create(self)
		self.search = search.Search(self)

		# nav bar
		self.nav   = tk.Frame(self,bg='gray',borderwidth=2,relief='groove')
		self.h_title = tk.Label(self,font=('Arial',14,'bold'),text='loggr v5.0')

		# nav buttons
		self.btn_s = tk.Button(self.nav,text='Search')
		self.btn_c = tk.Button(self.nav,text='Create')

		# config
		self.btn_s.id = 'search'
		self.btn_c.id = 'create'
		self.btn_s.bind('<Button-1>', self.get_screen)
		self.btn_c.bind('<Button-1>', self.get_screen)
		self.btn_s.configure(font=('Arial',12,'bold'),fg='black',bg='light gray',width=6,borderwidth=2,relief='groove')
		self.btn_c.configure(font=('Arial',12,'bold'),fg='black',bg='light gray',width=6,borderwidth=2,relief='groove')

		# self.nav grid
		self.btn_s.grid(row=0,column=0,padx=4,pady=4)
		self.btn_c.grid(row=0,column=2)

		# main window placement
		self.h_title.pack(padx=5,pady=3,anchor='w')
		self.nav.pack(fill='x')
		self.main.pack(anchor='s')

		# currently displayed screen
		self.screen_id = self.main

	def get_screen(self,event):
		''' get screen based on nav button click '''
		self.screen_id.pack_forget()
		self.screen_id.reset()

		if event.widget.id == 'create':
			self.create.pack(anchor='sw',pady=(10,0))
			self.screen_id = self.create
		elif event.widget.id == 'search':
			self.search.pack(anchor='sw',pady=(10,0))
			self.screen_id = self.search

root = Window()
root.mainloop()
