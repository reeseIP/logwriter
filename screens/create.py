import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
import screens.base as base

'''
	screens/create.py
'''

class Create(tk.Frame):
	''' main class for create screen elements '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)

		# screen globals
		self.parent = ''
		self.stories = []
		self.transports = []
		self.objects = []
		self.files = []
		self.charms = []

		# maintain connection to DB from master
		self.db_conn = self.master.db_conn

		# screen objects
		self.parent_entry = ParentEntry(self)
		self.story_entry 	= StoryEntry(self)
		self.story_records = StoryRecords(self)
		self.change_entry 	= ChangeEntry(self)
		self.change_records = ChangeRecords(self)
		self.object_entry	  = ObjectEntry(self)
		self.object_records = ObjectRecords(self)
		self.file_entry 		= FileEntry(self)
		self.file_records 	= FileRecords(self)
		self.main_buttons   = MainButtons(self)
		self.validation 		= self.master.validation

		# set the initial display
		#self.parent_entry.grid(row=0,padx=10,pady=5,sticky='w')
		#self.story_records.grid(row=1,padx=10,pady=5,sticky='nsew')
		#self.change_records.grid(row=2,padx=10,pady=5,sticky='w')
		#self.object_records.grid(row=3,padx=10,pady=5,sticky='w')
		#self.file_records.grid(row=4,padx=10,pady=5,sticky='w')
		#self.main_buttons.grid(row=5,padx=10,pady=5)

		self.parent_entry.pack(side='top',fill='x',expand=True,padx=10,pady=5)
		self.story_records.pack(after=self.parent_entry,fill='x',expand=True,padx=10,pady=5)
		self.change_records.pack(after=self.story_records,fill='x',expand=True,padx=10,pady=5)
		self.object_records.pack(after=self.change_records,fill='x',expand=True,padx=10,pady=5)
		self.file_records.pack(after=self.object_records,fill='x',expand=True,padx=10,pady=5)
		self.main_buttons.pack(after=self.file_records,fill='x',expand=True,padx=10,pady=5)
		

	def reset(self):
		''' reset the screen to initial settings '''
		self.main_buttons.cancel()


class ParentEntry(base.ParentEntry):
	''' parent entry '''

	def update_parent(self,event=None):
		if self.ent_parent.get():
			self.ent_parent.configure(state='disabled')
			self.master.parent = self.ent_parent.get()

	def reset_fields(self,event=None):
		self.ent_parent.configure(state='normal')
		self.ent_parent.delete(0,'end')
		self.ent_descr.delete(0,'end')
		self.ent_parent.focus_set()


class StoryEntry(base.StoryEntry):
	''' change entry '''

	def submit(self,event=None):
		''' submit button event handler '''
		story = self.ent_story.get().strip('\n')
		charm = self.ent_charm.get().strip('\n')
		descr = self.ent_descr.get().strip('\n')

		self.master.stories.append({'parent':self.master.parent,
																'story':story,
																'description':descr})

		charms = [item['charm'] for item in self.master.charms]
		if charm not in charms:
			# add new charm & transport to master list
			self.master.charms.append({'story':story,
																 'charm':charm,
																 'description':descr})

		self.master.story_records.add_story()
		self.cancel()

	def cancel(self,event=None):
		''' cancel '''
		self.ent_story.delete(0,'end')
		self.ent_charm.delete(0,'end')
		self.ent_descr.delete(0,'end')
		self.wm_withdraw()

	def new_story(self):
		''' new story '''
		if self.master.parent:
			x = self._root().winfo_x()
			y = self._root().winfo_y()
			self.geometry("+%d+%d" %(x+200,y+200))
			self.wm_deiconify()
		else:
			alert = messagebox.showerror('Error','Please enter a parent')


class StoryRecords(base.StoryRecords):
		''' change entry data '''

		def new_story(self,event=None):
			''' new story '''
			self.master.story_entry.new_story()

		def add_story(self,event=None):
			''' add story '''
			for item in self.window.winfo_children():
				item.destroy()

			for item in self.master.charms:
				# row for table
				row = tk.Frame(self.window)

				# story & description
				cbtn_sel   = tk.Checkbutton(row,width=1,height=1,anchor='nw',text=' ')
				lbl_story = tk.Label(row,text=item['story'],width=13,anchor='w')
				lbl_charm = tk.Label(row,text=item['charm'],width=12,anchor='w')
				lbl_descr = tk.Label(row,text=item['description'],anchor='w')

				# config
				cbtn_sel.name = 'sel'
				lbl_story.name = 'story'
				lbl_charm.name = 'charm'
				lbl_descr.name = 'descr'
				row.id = self.row_index

				cbtn_sel.sel = tk.StringVar()
				cbtn_sel.configure(variable=cbtn_sel.sel)
				cbtn_sel.sel.set(0)
				cbtn_sel.id = {'story':item['story'],'charm':item['charm']}
				cbtn_sel.bind('<ButtonRelease-1>',self.selection)

				# grid
				row.grid(row=self.row_index,column=0,pady=(2,0),sticky='w')
				cbtn_sel.grid(row=0,column=0,padx=(5,0))
				lbl_story.grid(row=0,column=1)
				lbl_charm.grid(row=0,column=2)
				lbl_descr.grid(row=0,column=3,sticky='ew')

				self.row_index = self.row_index + 1

			self.update_idletasks()
			self.set_scroll()
			self.canvas.unbind('<Configure>')

		def reset_fields(self):
			''' reset fields '''
			self.row_index = 0
			for item in self.window.winfo_children():
				item.destroy()

		def selection(self,event=None):
			''' move selected object to the entry view '''
			storyId = event.widget.id

			if self.sel_row:
				if self.sel_row.id == storyId:
					self.sel_row = None
				else:
					self.sel_row = event.widget
			else:
				self.sel_row = event.widget

			for item in self.window.winfo_children():
				for row in item.winfo_children():
					if '!checkbutton' in str(row):
						if self.sel_row:
							if self.sel_row.id != row.id:
								row.deselect()

		def remove(self,event=None,changeId=None):
			''' remove '''
			if not changeId:
				changeId = self.sel_row.id

			# charm table delta updates
			for change in self.master.charms[:]:
				if change['charm'] == changeId['charm']:
					self.master.charms.remove(change)

			for change in self.master.stories[:]:
				if change['story'] == changeId['story']:
					self.master.stories.remove(change)

			[self.master.change_records.remove(event=None,changeId={'transport':change['transport']}) 
				for change in self.master.transports if change['charm'] == changeId['charm']]

			self.add_story()
			self.update_idletasks()
			self.set_scroll()
			self.sel_row = None


class ChangeEntry(base.ChangeEntry):
	''' change entry '''

	def submit(self,event):
		''' top level submit event '''
		charm = self.v_charm.get().strip('\n')
		trans = self.ent_trans.get().strip('\n')
		descr = self.ent_descr.get().strip('\n')

		for item in self.master.transports:
			if item['transport'] == trans:
				alert = messagebox.showerror('Error','Transport already created in session!')
				return

		if True == True:
		#if self.master.validation.validate_charm_and_tran(charm,trans,descr):

			self.master.transports.append({'parent':self.master.parent,
																		 'transport':trans,
																		 'charm':charm,
																		 'description':descr})

			self.cancel()
			self.master.change_records.set_display()

	def cancel(self,event=None):
		''' top cancel '''
		self.wm_withdraw()
		self.v_charm.set('Select a Charm')
		self.ent_trans.delete(0,'end')
		self.ent_descr.delete(0,'end')

	def new_change(self):
		''' new change '''
		if self.master.parent:
			charms = [item['charm'] for item in self.master.charms]
			self.opt_charm['menu'].delete(0,'end')
			for item in charms:
				self.opt_charm['menu'].add_command(label=item,command=tk._setit(self.v_charm,item))
			x = self._root().winfo_x()
			y = self._root().winfo_y()
			self.geometry("+%d+%d" %(x+200,y+200))
			self.wm_deiconify()
		else:
			alert = messagebox.showerror('Error','Please enter a parent')


class ChangeRecords(base.ChangeRecords):
	''' view for charm records '''

	def add(self,event):
		''' add charm & transport '''
		self.master.change_entry.new_change()

	def remove(self,event):
		''' remove charm & transport '''
		pass

	def set_display(self):
		''' add items to the parent and charm/transport view '''
		self.reset_fields()
		for item in self.master.transports:
			line = tk.Frame(self.charms)
			line.id = item['transport']
			cbtn_sel   = tk.Checkbutton(line,width=1,height=1,anchor='nw',text=' ')
			lbl_charm = tk.Label(line,anchor='w',width=12,text=item['charm'])
			lbl_trans = tk.Label(line,anchor='w',width=12,text=item['transport'])
			lbl_descr = tk.Label(line,anchor='w',text=item['description'])
			line.grid(row=self.row_index,column=0,pady=(2,0),sticky='w')
			cbtn_sel.grid(row=0,column=0,padx=(5,0))
			lbl_charm.grid(row=0,column=1)
			lbl_trans.grid(row=0,column=2)
			lbl_descr.grid(row=0,column=3,sticky='ew')

			cbtn_sel.sel = tk.StringVar()
			cbtn_sel.configure(variable=cbtn_sel.sel)
			cbtn_sel.sel.set(0)

			cbtn_sel.id = {'transport':item['transport'],'charm':item['charm']}

			cbtn_sel.bind('<ButtonRelease-1>',self.selection)

			self.row_index = self.row_index + 1

		# update the scrollregion
		self.update_idletasks()
		self.set_scroll()

	def reset_fields(self):
		''' reset the data '''
		for item in self.charms.winfo_children():
			item.destroy()

	def selection(self,event=None):
		''' move selected object to the entry view '''
		changeId = event.widget.id

		if self.sel_row:
			if self.sel_row.id == changeId:
				self.sel_row = None
			else:
				self.sel_row = event.widget
		else:
			self.sel_row = event.widget

		for item in self.charms.winfo_children():
			for row in item.winfo_children():
				if '!checkbutton' in str(row):
					if self.sel_row:
						if self.sel_row.id != row.id:
							row.deselect()

	def remove(self,event=None,changeId=None):
		''' remove '''
		if not changeId:
			changeId = self.sel_row.id

		# object table delta updates
		for change in self.master.transports[:]:
			if change['transport'] == changeId['transport']:
				self.master.transports.remove(change)

		[self.master.object_records.remove_obj_from_view(event=None,objectId=obj['objectId']) 
			for obj in self.master.objects if obj['transport'] == changeId['transport']]

		self.set_display()
		self.update_idletasks()
		self.set_scroll()
		self.sel_row = None


class ObjectEntry(base.ObjectEntry):
		''' object data entry '''

		def add_obj(self,event=None):
			''' add obj '''
			transport = self.v_trans.get().strip('\n')
			objectType = self.v_objty.get().strip('\n')
			objectName = self.ent_obj.get().strip('\n')
			description = self.txt_desc.get(1.0,'end')

			if True == True:
			#if self.master.validation.validate_obj_data(transport,
			#																						 objectType,
			#																						 objectName,
			#																						 description):
				if self.master.object_records.sel_row:
					objectId = self.master.object_records.sel_row.id
					if objectId or objectId == 0:
					# add this to the validation class
						for item in self.master.objects:
							if item['objectId'] == objectId:
								alert = messagebox.askyesno('Warning','Overwrite Entry?')
								if alert == True:
									item['transport'] = transport
									item['objectType'] = objectType
									item['objectName'] = objectName
									item['description'] = description

									for file in self.master.files:
										if objectId == file['objectId']:
											file['transport'] = transport
											file['objectName'] = objectName

									self.master.file_records.add_file_to_view()
									self.master.object_records.add_obj_to_view()
									self.master.object_records.sel_row = None
									self.close_window()
									return
								else:
									return

				# add created objects to master dict
				self.master.objects.append({'parent': self.master.parent,
																		'objectId':self.object_id,
																		'transport':transport,
																		'objectType':objectType,
																		'objectName':objectName,
																		'description':description})

				# create the object table and add new object to view
				self.master.file_records.add_file_to_view()
				self.master.object_records.add_obj_to_view(self.object_id)
				self.master.object_records.sel_row = None
				self.object_id = self.object_id + 1

			self.close_window()
			
		def reset_fields(self,event=None):
			''' reset fields '''
			# reset the object and transport field state
			self.v_trans.set('Select a Transport')
			self.v_objty.set('Select an Object Type')
			self.ent_obj.delete(0,'end')
			self.txt_desc.delete(1.0,'end')
			if event:
				self.grid_remove()

		def new_object(self,event=None):
			if self.master.parent:
				transports = [item['transport'] for item in self.master.transports]
				self.opt_trans['menu'].delete(0,'end')
				for item in transports:
					self.opt_trans['menu'].add_command(label=item,command=tk._setit(self.v_trans,item))
				self.reset_fields()
				x = self._root().winfo_x()
				y = self._root().winfo_y()
				self.geometry("+%d+%d" %(x+200,y+200))
				self.deiconify()
				self.grab_set()
			else:
				alert = messagebox.showerror('Error','Please enter a parent')

		def close_window(self,event=None):
			self.reset_fields()
			self.grab_release()
			self.wm_withdraw()


class ObjectRecords(base.ObjectRecords):
		''' view for session added objects '''

		def add_obj_to_view(self,objectId=None):
			''' add object to view '''
			self.reset_fields()
			for item in self.master.objects:
				line = tk.Frame(self.objects)
				line.id = item['objectId']
				cbtn_sel   = tk.Checkbutton(line,width=1,height=1,anchor='nw',text=' ')
				lbl_tran  = tk.Label(line,width=12,anchor='nw',text=item['transport'])
				lbl_objty = tk.Label(line,width=16,anchor='nw',text=item['objectType'])
				lbl_obj   = tk.Label(line,width=30,anchor='nw',text=item['objectName'])
				lbl_desc  = tk.Label(line,anchor='nw',text=item['description'].strip('\n'))

				# config
				cbtn_sel.sel = tk.StringVar()
				cbtn_sel.configure(variable=cbtn_sel.sel)
				cbtn_sel.sel.set(0)
				
				# set an index for table row reference
				cbtn_sel.id = item['objectId']
				cbtn_sel.name  = 'sel'
				lbl_tran.name  = 'transport'
				lbl_objty.name = 'objectType'
				lbl_obj.name   = 'objectName'
				lbl_desc.name  = 'description'

				# bind button one click event for selecting table row
				cbtn_sel.bind('<ButtonRelease-1>',self.sel_obj)

				# grid placement
				cbtn_sel.grid(row=0,column=0)
				lbl_tran.grid(row=0,column=1)
				lbl_objty.grid(row=0,column=2)
				lbl_obj.grid(row=0,column=3)
				lbl_desc.grid(row=0,column=4,sticky='ew')

				line.grid(row=self.row_index,column=0,sticky='w')

				# increment table row index
				self.row_index = self.row_index + 1

			# update scrollregion
			self.update_idletasks()
			self.set_scroll()

		def call_object_entry(self,event): #+++
			''' get the object entry frame '''
			self.master.object_entry.new_object()

		def reset_fields(self):
			''' reset fields '''
			# remove all items on object table
			for widget in self.objects.winfo_children():
				if widget._name != 'header':
					widget.destroy()
			self.sel_row = None

		def sel_obj(self,event):
			''' select object '''
			objectId = event.widget.id

			if self.sel_row:
				if self.sel_row.id == objectId:
					self.sel_row = None
				else:
					self.sel_row = event.widget
			else:
				self.sel_row = event.widget

			for item in self.objects.winfo_children():
				for row in item.winfo_children():
					if '!checkbutton' in str(row):
						if self.sel_row:
							if self.sel_row.id != row.id:
								row.deselect()

		def remove_obj_from_view(self,event=None,objectId=None):
			''' remove object from view '''
			# get the selected object
			if objectId == 0:
				objectId = 0
			elif not objectId:
				objectId = self.sel_row.id
			
			# object table delta updates
			for obj in self.master.objects[:]:
				 if obj['objectId'] == objectId:
				 	self.master.objects.remove(obj)

			#[self.master.objects.remove(obj) for obj in self.master.objects if obj['objectId'] == objectId]
			self.master.file_records.remove_file(event=None,objectId=objectId)

			self.add_obj_to_view()
			self.update_idletasks()
			self.set_scroll()
			self.sel_row = None

		def edit_entry(self,event=None):
			''' edit entry '''
			if self.sel_row or self.sel_row == 0:
				self.master.object_entry.new_object()
				self.master.object_entry.grab_set()
				for item in self.main.winfo_children():
					if item.id == self.sel_row:
						for row in item.winfo_children():
							if row.name == 'transport':
								self.master.object_entry.v_trans.set(row['text'])
							elif row.name == 'objectType':
								self.master.object_entry.v_objty.set(row['text'])
							elif row.name == 'objectName':
								self.master.object_entry.ent_obj.insert(0,row['text'])
							elif row.name == 'description':
								self.master.object_entry.txt_desc.insert(0.0,row['text'])
			else:
				messagebox.showwarning('Warning','Please select an entry to edit.')


class FileEntry(base.FileEntry):
	''' file entry '''

	def submit(self,event):
		# add attached files to master list
		if self.lbl_file['text']:
			self.master.files.append({'parent':self.master.parent,
																'objectId':self.objectId,
																'objectName':self.objectName,
																'transport':self.transport,
																'dFileName':self.dfile_name,
																'dFilePath':self.dfile_file,
																'dFileId':self.dfile_id,
																'dFileCont':self.dfile_cont})

			# create attached files table and add selected file
			self.master.file_records.add_file_to_view()

			self.objectId = ''
			self.objectName = ''
			self.transport = ''
			self.dfile_file = ''
			self.dfile_name =''
			self.dfile_id = ''
			self.dfile_cont = ''

			self.wm_withdraw()
			self.cancel()

	def select(self,event):
		''' top submit '''
		self.objectName = self.v_object.get().strip('\n')
		self.transport = self.v_transport.get().strip('\n')
		# ensure that the object & transport are entered
		if self.objectName != 'Select an Object' and self.transport != 'Select a Transport':
			self.objectId = [item['objectId'] for item in self.master.objects if item['objectName'] == self.objectName]
			if not self.objectId:
				self.objectId = self.object_id
			else:
				self.objectId = self.objectId[0]
			# source file
			try:
				with askopenfile() as file:
					sfile_name = self.parse_file_name(file.name)
					sfile_cont = file.read()

					# destination file, store values for save function
					self.dfile_name = sfile_name
					self.lbl_file.configure(text=sfile_name)
					self.dfile_cont = sfile_cont
					self.dfile_id = ''.join(random.choices(string.ascii_lowercase,k=20))
					self.dfile_file = self.master.master.file_dir / self.dfile_id

			except(AttributeError):
				return
			self.focus_set()
		else:
			alert = messagebox.showerror('Error','Transport and Object must be filled!')
			self.focus_set()

	def cancel(self,event=None):
		''' top cancel '''
		self.v_transport.set('Select a Transport')
		self.v_object.set('Select an Object')
		self.lbl_file.configure(text='')
		self.wm_withdraw()

	def list_obj(self,event,callback,mode):
		self.opt_obj['menu'].delete(0,'end')
		objects = [item['objectName'] for item in self.master.objects if item['transport'] == self.v_transport.get()]
		for item in objects:
			self.opt_obj['menu'].add_command(label=item,command=tk._setit(self.v_object, item))

	def new_file(self,event=None):
		''' attach file '''
		if self.master.parent:
			self.opt_trans['menu'].delete(0,'end')
			transports = [item['transport'] for item in self.master.transports]
			for item in transports:
				self.opt_trans['menu'].add_command(label=item,command=tk._setit(self.v_transport, item))

			x = self._root().winfo_x()
			y = self._root().winfo_y()
			self.geometry("+%d+%d" %(x+200,y+200))
			self.wm_deiconify()
		else:
			alert = messagebox.showerror('Error','Please enter a parent')

	def parse_file_name(self,file_name):
		''' parse file name '''
		# get a list of chars in file path
		letters = list(file_name)

		# get the file name, delete rest of path
		locs = []
		index = -1
		for c in letters:
			if c == '/':
				locs.append(letters.index(c,index+1))
			index = letters.index(c,index+1)
		del letters[0:locs[-1]+1]

		# reconstruct file name
		file = ''
		for c in letters:
			file = file + c
		return file


class FileRecords(base.FileRecords):
		''' view for session attached files '''

		def attach_file(self,event):
			''' attach file '''
			self.master.file_entry.new_file()

		def add_file_to_view(self):
			''' add file to view '''
			self.reset_fields()
			for item in self.master.files:
				if True == True:
					# file name, object, transport
					line = tk.Frame(self.files)
					cbtn_sel = tk.Checkbutton(line,width=1,height=1,state='normal',anchor='nw')
					lbl_fname = tk.Label(line,height=1,anchor='nw',text=item['dFileName'])
					lbl_obj   = tk.Label(line,width=30,height=1,anchor='nw',text=item['objectName'])
					lbl_tran  = tk.Label(line,width=12,height=1,anchor='nw',text=item['transport'])

					# config
					cbtn_sel.sel = tk.StringVar()
					cbtn_sel['variable'] = cbtn_sel.sel
					cbtn_sel.sel.set(0)

					cbtn_sel.id = item['objectId']
					cbtn_sel.name  = item['dFileName']
					#lbl_fname.name = item['dFileName']
					#lbl_obj.name   = item['dFileName']
					#lbl_tran.name  = item['dFileName']

					cbtn_sel.bind('<ButtonRelease-1>',self.select_file)

					# grid placement
					cbtn_sel.grid(row=0,column=0)
					lbl_tran.grid(row=0,column=1)
					lbl_obj.grid(row=0,column=2)
					lbl_fname.grid(row=0,column=3,sticky='ew')

					line.grid(row=self.row_index,column=0,sticky='w')

					# increment table row index
					self.row_index = self.row_index + 1

			# update scrollregion
			self.update_idletasks()
			self.set_scroll()

		def select_file(self,event=None):
			objectId = event.widget.id
			fileName = event.widget.name

			if self.sel_row:
				if self.sel_row.id == objectId and self.sel_row.name == fileName:
					self.sel_row = None
				else:
					self.sel_row = event.widget
			else:
				self.sel_row = event.widget

			for item in self.files.winfo_children():
				for row in item.winfo_children():
					if '!checkbutton' in str(row):
						if self.sel_row:
							if self.sel_row.id == row.id and self.sel_row.name == row.name:
								pass
							else:
								row.deselect()

		def remove_file(self,objectId=None,event=None):
			''' remove file '''
			if objectId or objectId == 0:
				# file table delta updates
				for file in self.master.files[:]:
					if file['objectId'] == objectId:
						self.master.files.remove(file)

			else:
				objectId = self.sel_row.id
				fileName = self.sel_row.name
				# remove item from view, then from the master file list
				for file in self.master.files[:]:
					if file['objectId'] == objectId and file['dFileName'] == fileName:
						self.master.files.remove(file)

			# update scrollregion
			self.sel_row = None
			self.add_file_to_view()
			self.update_idletasks()
			self.set_scroll()

		def reset_fields(self):
			''' reset fields '''
			for widget in self.files.winfo_children():
				widget.destroy()
			self.sel_row = None


class MainButtons(base.MainButtons):
	''' buttons for primary functions like saving log and cancel '''

	def cancel(self,event=None):
		''' cancel log '''
		self.master.parent = ''
		self.master.stories.clear()
		self.master.charms.clear()
		self.master.objects.clear()
		self.master.files.clear()
		self.master.transports.clear()
		self.master.parent_entry.reset_fields()
		self.master.story_records.reset_fields()
		self.master.change_records.reset_fields()
		self.master.object_records.reset_fields()
		self.master.object_entry.reset_fields()
		self.master.file_records.reset_fields()
		self.master.file_entry.wm_withdraw()
		self.master.change_entry.wm_withdraw()
		self.master.object_entry.wm_withdraw()

	def save_log(self,event=None):
		''' save log '''

		# add logic to update parent table 
		if True == True:
		#if self.master.validation.validate_parent_data(self.ent_parent.get(),
		#																								self.ent_story.get(),
		#																								self.ent_p_descr.get()):
			# set parent and lock entry
			#self.master.parent_entry.ent_parent.configure(state='disabled')
			#self.master.parent = self.master.parent_entry.ent_parent.get()

			story = None
			description = None
			descriptions = [story['description'] for story in self.master.stories]

			# get a list of stories that have been entered, add to master list
			self.master.stories.clear()
			for item in self.master.story_records.window.winfo_children():
				for row in item.winfo_children():
					if row.name == 'story':
						story = row['text']
					elif row.name == 'descr':
						descr = row['text']
	
				self.master.stories.append({'parent':self.master.parent,
											'story':story,
											'description':descr})

		# validate no unsaved data
		if self.master.object_entry.ent_obj.get():
			error = True
			for item in self.master.objects:
				if item['objectName'] == self.master.object_entry.ent_obj.get():
					error = False
					
			if error:
				alert = messagebox.showerror('error','Save or cancel object before moving on')
				return
		elif self.master.parent_entry.ent_parent['state'] == 'normal':
			alert = messagebox.showerror('Error', 'Please submit parent information before saving!')
			return	

		# update parent table
		result = self.master.db_conn.insert_table('parent',[self.master.parent,self.master.parent_entry.ent_descr.get()])
		if result:
			alert = messagebox.showerror('Error',result)
			return

		# update note_header table
		result = self.master.db_conn.insert_table('note_header',[None,self.master.parent,self.master.parent_entry.ent_descr.get(),'Created','Development'])
		if result:
			alert = messagebox.showerror('Error',result)
			return
			
		# update story table
		#list_stories = [item for item in self.master.stories]
		stories = [list(item.values()) for item in self.master.stories]
		if stories:
			for item in stories:
				result = self.master.db_conn.insert_table('story',item)
				if result:
					alert = messagebox.showerror('Error',result)
					return
					
		# check if file already exists w/reference to key fields
		for row in self.master.files:
			file = row['dFilePath']
			try:
				file.touch(exist_ok=False)
			except(FileExistsError):
				alert = messagebox.showerror('Error','Error saving file!')
				return
				
			# write contents to new file
			with file.open(mode='w',encoding='utf-8') as ofile:
				ofile.write(row['dFileCont'])
				
			# change win path to string, remove file content
		for item in self.master.files:
			item['dFilePath'] = str(item['dFilePath'])
			
		# update files table
		files = [list(item.values()) for item in self.master.files]
		if files:
			for item in files:
				del item[7]
				result = self.master.db_conn.insert_table('files',item)
				if result:
					alert = messagebox.showerror('Error',result)
					return
				
		# update charm table
		charms = [list(item.values()) for item in self.master.charms]
		if charms:
			for item in charms:
				result = self.master.db_conn.insert_table('charm',[self.master.parent,item[0],item[1],item[2]])
				if result:
					alert = messagebox.showerror('Error',result)
					return
					
		# update transport tables
		transports = [list(item.values()) for item in self.master.transports]
		if transports:
			for item in transports:
				result = self.master.db_conn.insert_table('transport',item[0:4])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update object table
		objects = [list(item.values()) for item in self.master.objects]
		if objects:
			for item in objects:
				result = self.master.db_conn.insert_table('object',item)
				if result:
					alert = messagebox.showerror('Error',result)
					return

		self.cancel()