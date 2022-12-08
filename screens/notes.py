import os
import pathlib
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile

'''
	screens/main.py
'''

class Notes(tk.Frame):
	''' main landing screen for loggr '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)
		
		# variables
		self.noteEntry = NoteEntry(self)
		self.notes = []
		self.deltaNotes = []
		self.statuses = ['Created','In Progress','Complete']
		self.systems = ['Development','Quality','Pre-Prod','Production']
		self.index = 0

		# main objects
		self.main = tk.Frame(self)

		# self.main objects
		self.work = tk.Frame(self.main)
		self.work.configure(borderwidth=2,relief='groove')

		self.display()

		# main grid
		self.main.grid(row=0,column=0,sticky='w')

		# self.main grid
		self.work.grid(row=0,column=0,padx=5,pady=5,sticky='w')

	def new_note(self,event=None):
		id = event.widget.id
		self.noteEntry.new_note(id)

	def select(self,event=None):
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				for x in row.winfo_children():
					if '!optionmenu' in str(x):
						print(x.getvar(x['textvariable']))

	def display(self,event=None):
		self.reset_fields()
		for item in self.master.db_conn.select_table('note_header').fetchall():
			# row for the note_header level
			row = tk.Frame(self.work)
			row.id = item[0]
			# frames for the optionmenus, notes
			options = tk.Frame(row)
			notes = tk.Frame(row)
			
			# parent and description
			text = '{} - {}'.format(item[1],item[2])
			pLine = tk.Label(row,text=text)

			# status and system
			varStatus = tk.StringVar()
			varSystem = tk.StringVar()
			varStatus.set(item[3])
			varSystem.set(item[4])
			lblStatus = tk.Label(options,text='Status')
			lblSystem = tk.Label(options,text='System')
			optStatus = tk.OptionMenu(options,varStatus,item[3],*[s for s in self.statuses if s != item[3]])
			optSystem = tk.OptionMenu(options,varSystem,item[4],*[s for s in self.systems if s != item[4]])
			varStatus.trace_add('write',self.update_status)
			varSystem.trace_add('write',self.update_system)

			pLine.grid(row=0,column=0,sticky='w')
			#status.bind('<Button-1>',self.select)

			# stories, charms, description
			index = 1
			for charm in self.master.db_conn.select_table('charm','parent',item[1]).fetchall():
				text = '{} - {} - {}'.format(charm[1],charm[2],charm[3])
				cLine = tk.Label(row,text=text)
				cLine.grid(row=index,column=0,sticky='w')
				index = index + 1

			notesHeader = tk.Frame(notes)
			lblNotes = tk.Label(notesHeader,text='Notes:')
			btnPlus = tk.Button(notesHeader,text='+')
			btnPlus.id = item[0]
			btnPlus.bind('<Button-1>',self.new_note)
			lblNotes.grid(row=0,column=0,padx=(0,2),sticky='w')
			btnPlus.grid(row=0,column=1,padx=2,sticky='e')
			notesHeader.grid(row=0,column=0,sticky='w')

			notesMain = tk.Frame(notes)
			idx = 0
			for note in self.master.db_conn.select_table('notes','noteid',str(item[0])).fetchall():
				noteLine = tk.Frame(notesMain)
				btnMinus = tk.Button(noteLine,text='-')
				lblDate = tk.Label(noteLine,text=note[2])
				lblNote = tk.Label(noteLine, text=note[1].strip('\n'),wraplength=300)
				btnMinus.id = [note]
				btnMinus.bind('<Button-1>',self.delete_note)
				btnMinus.grid(row=0,column=0,sticky='nw')
				lblDate.grid(row=0,column=1,sticky='nw')
				lblNote.grid(row=0,column=2,sticky='nw')
				noteLine.grid(row=idx,column=0,sticky='nw')
				idx = idx + 1
			idx = 0
			notesMain.grid(row=1,column=0,sticky='w')

			# options grid
			lblStatus.grid(row=0,column=0,sticky='w')
			optStatus.grid(row=0,column=1,sticky='w')
			lblSystem.grid(row=1,column=0,sticky='w')
			optSystem.grid(row=1,column=1,sticky='w')
			# row grid
			options.grid(row=index+1,column=0,sticky='w')
			notes.grid(row=index+2,column=0,sticky='w')
			# self.work grid
			row.grid(row=self.index,column=0,padx=(5,10),pady=(5,15),sticky='w')

			# reset charm index, increment header index
			index = 1
			self.index = self.index + 1
		#index = 0
		#for note in self.notes:
		#	lblNote = tk.Label(notesMain,text=note['notetxt'])
		#	lblNote.grid(row=index)
		#	index = index + 1
#
		#index = 0

	def delete_note(self,event=None):
		id = event.widget.id
		result = self.master.db_conn.delete_table('notes','created',value=id)
		self.display()

	def reset_fields(self):
		for item in self.work.winfo_children():
			item.destroy()

	def reset(self):
		for item in self.work.winfo_children():
			item.destroy()
		self.display()

	def update_status(self,callback=None,mode=None,event=None):
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				for x in row.winfo_children():
					for i in x.winfo_children():
						if '!optionmenu' in str(i):
							if i['textvariable'] == callback:
								result = self.master.db_conn.update_table('note_header','status',i.getvar(i['textvariable']),'noteid',row.id)

	def update_system(self,callback=None,mode=None,event=None):
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				for x in row.winfo_children():
					for i in x.winfo_children():
						if '!optionmenu' in str(i):
							if i['textvariable'] == callback:
								result = self.master.db_conn.update_table('note_header','system',i.getvar(i['textvariable']),'noteid',row.id)

class NoteEntry(tk.Toplevel):
	''' note entry '''

	def __init__(self,*args,**kwargs):
		tk.Toplevel.__init__(self,*args,**kwargs)
		self.noteid = None
		self.wm_withdraw()
		self.protocol('WM_DELETE_WINDOW',self.cancel)

		self.header = tk.Frame(self)

		self.lblNote = tk.Label(self.header,text='Note')
		self.btnSubmit = tk.Button(self.header,text='Submit')
		self.lblNote.grid(row=0,column=0,padx=(5,2),sticky='w')
		self.btnSubmit.grid(row=0,column=1,padx=2,sticky='w')
		self.header.grid(row=0,column=0)

		self.txtNote = tk.Text(self,wrap='word')
		self.txtNote.grid(row=1,column=0)

		self.btnSubmit.bind('<Button-1>',self.submit)

	def cancel(self,event=None):
		self.wm_withdraw()
		self.noteid = None
		self.txtNote.delete(0.0,'end')

	def new_note(self,noteid,event=None):
		self.noteid = noteid
		x = self._root().winfo_x()
		y = self._root().winfo_y()
		self.geometry("+%d+%d" %(x+200,y+200))
		self.wm_deiconify()

	def submit(self,event=None):
		text = self.txtNote.get(0.0,'end')
		result = self.master.master.db_conn.insert_table('notes',[self.noteid,text,datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S")])
		self.master.display()
		self.cancel()