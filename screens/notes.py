import os
import pathlib
import datetime
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from tkinter import *

'''
	screens/main.py
'''

class Notes(tk.Frame):
	''' main landing screen for loggr '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)
		
		# objects
		self.noteEntry = NoteEntry(self)
		self.app_path = self.master.app_path
		self.db_conn = self.master.db_conn

		# variables
		self.index = 1
		
		# lists
		self.notes = []
		self.statuses = ['Created','In Progress','Complete']
		self.systems = ['Development','Quality','Pre-Prod','Production']

		# icons for buttons
		self.iconTrash = PhotoImage(file=self.app_path.joinpath(pathlib.Path('img\\trash.png')))
		self.iconCreate = PhotoImage(file=self.app_path.joinpath(pathlib.Path('img\\edit-file.png')))

		# main objects
		self.main = tk.Frame(self)
		self.frNotepad = tk.Frame(self)

		# self.main objects, open & completed work
		self.work = tk.Frame(self.main)
		self.comp = tk.Frame(self.main)
		self.workHeader = tk.Label(self.main,text='Open Work:')
		self.compHeader = tk.Label(self.main,text='Completed:')

		# self.frNotepad objects
		self.notepad = tk.Text(self.frNotepad)

		# config
		self.main.configure(width=1000,borderwidth=2,relief='groove')
		self.frNotepad.configure(borderwidth=2,relief='groove')
		self.work.configure(borderwidth=2,relief='groove')
		self.comp.configure(borderwidth=2,relief='groove')
		self.notepad.configure(wrap='word',width=50)
		# get the contents of the notepad from the database
		text = self.db_conn.select_table('notepad').fetchone()[0].strip('\n')
		self.notepad.insert(0.0,text)

		# events
		self.bind('<Configure>',self.update_notepad)

		# main pack
		self.main.pack(side='left',anchor='nw',fill='x')
		self.frNotepad.pack(side='left',after=self.main,anchor='nw',fill='x',expand=True)

		# self.main pack
		self.workHeader.pack(side='top',anchor='w',padx=3,pady=(10,0))
		self.work.pack(side='top',after=self.workHeader,padx=5,pady=5,anchor='nw',fill='x')
		self.compHeader.pack(side='top',after=self.work,anchor='w',padx=3,pady=(10,0))
		self.comp.pack(side='top',after=self.compHeader,padx=5,pady=5,anchor='nw',fill='x')

		# self.frNotepad grid
		self.notepad.pack(anchor='w',fill='x',expand=True)

		self.display()

	def new_note(self,event=None):
		''' new note '''
		# get the id associated with the note_header and call noteEntry,
		# the id is assigned in .display()
		id = event.widget.id
		self.noteEntry.new_note(id)

	def display(self,event=None):
		''' display '''
		self.reset_fields()
		for item in self.db_conn.select_table('note_header').fetchall():
			if item[3] == 'Complete':
				row = tk.Frame(self.comp) # assign to complete work
			else:
				row = tk.Frame(self.work) # assign to open work

			row.id = item[0] # set the row.id as the note_id
			row.configure(bd=2,relief='groove')


			# row objects
			options = tk.Frame(row)
			notes = tk.Frame(row) # frames for the optionmenus, notes

			# notesHeader and notes objects
			notesHeader = tk.Frame(notes)
			notesMain = tk.Frame(notes)
			lblNotes = tk.Label(notesHeader)
			btnPlus = tk.Button(notesHeader)
			
			# parent and description
			text = '{} - {}'.format(item[1],item[2].strip('\n'))
			pLine = tk.Label(row,text=text)

			# status and system
			varStatus = tk.StringVar()
			varSystem = tk.StringVar()
			lblStatus = tk.Label(options)
			lblSystem = tk.Label(options)
			optStatus = tk.OptionMenu(options,varStatus,item[3],*[s for s in self.statuses if s != item[3]])
			optSystem = tk.OptionMenu(options,varSystem,item[4],*[s for s in self.systems if s != item[4]])

			# status and system config
			varStatus.set(item[3])
			varSystem.set(item[4])
			lblStatus.configure(text='Status',font=('Arial',10,'bold'))
			lblSystem.configure(text='System',font=('Arial',10,'bold'))
			optStatus.configure(borderwidth=0,height=0)
			optSystem.configure(borderwidth=0,height=0)
			varStatus.trace_add('write',self.update_status)
			varSystem.trace_add('write',self.update_system)

			# stories, charms, descriptions
			index = 1
			for charm in self.db_conn.select_table('charm','parent',item[1]).fetchall():
				text = '{} - {} - {}'.format(charm[1],charm[2],charm[3].strip('\n'))
				cLine = tk.Label(row,text=text)
				cLine.grid(row=index,column=0,sticky='w')
				index = index + 1

			# notes
			idx = 0
			for note in self.db_conn.select_table('notes','noteid',str(item[0])).fetchall():
				noteLine = tk.Frame(notesMain)
				# button for deleting note, label for the date and note content
				btnMinus = tk.Button(noteLine,image=self.iconTrash,borderwidth=0)
				lblDate = tk.Label(noteLine,text=note[2])
				lblNote = tk.Label(noteLine, text=note[1].strip('\n'),wraplength=400,justify='left')
				btnMinus.id = [note]
				btnMinus.bind('<Button-1>',self.delete_note)
				btnMinus.grid(row=0,column=0,sticky='nw')
				lblDate.grid(row=0,column=1,sticky='nw')
				lblNote.grid(row=0,column=2,sticky='nw')
				noteLine.grid(row=idx,column=0,sticky='nw')
				idx = idx + 1
			idx = 0

			# config
			btnPlus.id = item[0] # set the button.id as the note_id
			lblNotes.configure(text='Notes',font=('Arial',10,'bold'))
			btnPlus.configure(image=self.iconCreate,borderwidth=0)

			# events
			btnPlus.bind('<Button-1>',self.new_note)

			# self.work grid
			#row.grid(row=self.index,column=0,padx=(5,10),pady=(5,15),sticky='nsew')
			row.pack(anchor='w',fill='x')

			# row grid
			pLine.grid(row=0,column=0,sticky='w')
			options.grid(row=index+1,column=0,sticky='nsew')
			notes.grid(row=index+2,column=0,sticky='nsew')

			# options grid
			lblStatus.grid(row=0,column=0,sticky='w')
			optStatus.grid(row=0,column=1,sticky='nw')
			lblSystem.grid(row=1,column=0,sticky='w')
			optSystem.grid(row=1,column=1,sticky='nw')

			# notes grid
			notesHeader.grid(row=0,column=0,pady=(0,2),sticky='nsew')
			notesMain.grid(row=1,column=0,sticky='nsew')

			# notesHeader grid
			lblNotes.grid(row=0,column=0,padx=(0,2),sticky='nw')
			btnPlus.grid(row=0,column=1,padx=2,sticky='e')

			# reset charm index, increment header index
			index = 1
			self.index = self.index + 1

	def delete_note(self,event=None):
		''' delete note '''
		id = event.widget.id
		result = self.db_conn.delete_table('notes',value=id)
		self.display()

	def reset_fields(self):
		''' reset_fields '''
		for item in self.work.winfo_children():
			item.destroy()
		for item in self.comp.winfo_children():
			item.destroy()

	def reset(self):
		''' reset '''
		self.reset_fields()
		self.display()

	def update_status(self,callback=None,mode=None,event=None):
		''' update status '''
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				for x in row.winfo_children():
					for i in x.winfo_children():
						if '!optionmenu' in str(i):
							if i['textvariable'] == callback:
								result = self.db_conn.update_table('note_header',\
																						'status',i.getvar(i['textvariable']),'noteid',row.id)
		self.display()

	def update_system(self,callback=None,mode=None,event=None):
		''' update system '''
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				for x in row.winfo_children():
					for i in x.winfo_children():
						if '!optionmenu' in str(i):
							if i['textvariable'] == callback:
								result = self.db_conn.update_table('note_header',\
																						'system',i.getvar(i['textvariable']),'noteid',row.id)
		self.display()

	def update_notepad(self,event=None):
		''' update notepad '''
		self._root().after(60000,self.update_notepad)
		result = self.db_conn.update_table('notepad',
																'notetxt',self.notepad.get(0.0,'end'))
		result = self.db_conn.update_table('notepad',
																'changed',datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S"))


class NoteEntry(tk.Toplevel):
	''' note entry '''

	def __init__(self,*args,**kwargs):
		tk.Toplevel.__init__(self,*args,**kwargs)

		# variables
		self.noteid = None

		# main objects
		self.header = tk.Frame(self)
		self.txtNote = tk.Text(self)

		# self.header objects
		self.lblNote = tk.Label(self.header,text='Note')
		self.btnSubmit = tk.Button(self.header,text='Submit')

		# main grid
		self.header.grid(row=0,column=0)
		self.txtNote.grid(row=1,column=0)

		# self.header grid
		self.lblNote.grid(row=0,column=0,padx=(5,2),sticky='w')
		self.btnSubmit.grid(row=0,column=1,padx=2,sticky='w')

		# config
		self.wm_withdraw()
		self.protocol('WM_DELETE_WINDOW',self.cancel)
		self.txtNote.configure(wrap='word')

		# events
		self.btnSubmit.bind('<Button-1>',self.submit)

	def cancel(self,event=None):
		''' cancel '''
		self.wm_withdraw()
		self.noteid = None
		self.txtNote.delete(0.0,'end')

	def new_note(self,noteid,event=None):
		''' new note '''
		self.noteid = noteid
		x = self._root().winfo_x()
		y = self._root().winfo_y()
		self.geometry("+%d+%d" %(x+200,y+200))
		self.wm_deiconify()

	def submit(self,event=None):
		''' submit '''
		text = self.txtNote.get(0.0,'end')
		result = self.master.db_conn.insert_table('notes',\
																[self.noteid,text,datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S")])
		self.master.display()
		self.cancel()