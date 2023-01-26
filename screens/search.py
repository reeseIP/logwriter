import random
import string
import pathlib
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile, askdirectory
import screens.base as base

'''
	screens/search.py
'''

class Search(tk.Frame):
	''' main class for the search screen elements '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)

		# screen globals
		self.search_value = None
		self.parent = None
		self.parent_desc = None
		self.stories = []
		self.charms = []
		self.transports = []
		self.objects = []
		self.files = []

		# delta tables
		self.delta_parent = []
		self.delta_stories = []
		self.delta_charm = []
		self.delta_transport = []
		self.delta_object = []
		self.delta_files = []

		# query tables
		self.query_parent = []

		# maintain connection to DB from master
		self.db_conn = self.master.db_conn

		# screen objects
		self.notes = tk.Frame(self)
		self.validation     = self.master.validation
		self.query_result = QueryResult(self)
		self.parent_entry = ParentEntry(self)
		self.story_entry   = StoryEntry(self)
		self.story_records = StoryRecords(self)
		self.change_entry   = ChangeEntry(self)
		self.change_records = ChangeRecords(self)
		self.object_entry   = ObjectEntry(self)
		self.object_records = ObjectRecords(self)
		self.file_entry     = FileEntry(self)
		self.file_records   = FileRecords(self)
		self.main_buttons   = MainButtons(self)

	def reset(self):
		''' reset the screen to initial settings '''
		self.main_buttons.canc_log()

	def query(self):
		''' query '''
		validate = self.validation
		value = self.search_value
		query = None

		if not validate.validate_parent(value):
			query = validate.read_db('parent','parent',value)
		elif not validate.validate_story(value):
			query = validate.read_db('story','story',value)
		elif not validate.validate_charm(value):
			query = validate.read_db('charm','charm',value)
		elif not validate.validate_transport(value):
			query = validate.read_db('transport','transport',value)
		elif not validate.validate_object(value):
			query = validate.read_db('object','object_name',value)
			
		if query:
			self.query_result.display_result(query)
		else:
			self.query_result.display_result(None)


class QueryResult(tk.Frame):
	''' query result '''

	def __init__(self,*args,**kwargs):
		tk.Frame.__init__(self,*args,**kwargs)

		self.validate = self.master.validation
		self.main = tk.Frame(self)

		self.vscroll = tk.Scrollbar(self.main,orient='vertical')
		self.canvas = tk.Canvas(self.main,yscrollcommand=self.vscroll.set)

		self.vscroll.configure(command=self.canvas.yview)
		self.canvas.configure(scrollregion=(0,0,1000,1000))

		self.window = tk.Frame(self.canvas)

		self.canvas.create_window((0,0),window=self.window,anchor='nw',width=2000)
		self.main.pack(anchor='nw',side='left',fill='both',expand=True)

		self.canvas.pack(side='left',anchor='nw',fill='x',expand=True)
		self.canvas.bind('<Configure>',self.set_scroll)

	def display_result(self,query):
		''' display result '''
		self.reset_fields()
		if query:
			for item in query:
				parent = item[0]
				stories = [row[1] for row in self.validate.read_db('story','parent',parent)]
				charms = [row[2] for row in self.validate.read_db('charm','parent',parent)]
				transports = [row[1] for row in self.validate.read_db('transport','parent',parent)]
				objects = [row[4] for row in self.validate.read_db('object','parent',parent)]

				block = tk.Frame(self.window)
				block.id = parent
				block.bind('<Button-1>',self.get_item)
				lbl_parent = tk.Label(block,text='PARENT: ',font=('Arial',10,'bold'))
				lbl_stories = tk.Label(block,text='STORIES: ',font=('Arial',10,'bold'))
				lbl_charms = tk.Label(block,text='CHARMS: ',font=('Arial',10,'bold'))
				lbl_transports = tk.Label(block,text='TRANSPORTS: ',font=('Arial',10,'bold'))
				lbl_objects = tk.Label(block,text='OBJECTS: ',font=('Arial',10,'bold'))

				lbl_parent_val = tk.Label(block,text=parent)
				lbl_stories_val = tk.Label(block,text=stories)
				lbl_charms_val = tk.Label(block,text=charms)
				lbl_transports_val = tk.Label(block,text=transports)
				lbl_objects_val = tk.Label(block,text=objects)

				lbl_parent.grid(row=0,column=0,sticky='e')
				lbl_stories.grid(row=1,column=0,sticky='e')
				lbl_charms.grid(row=2,column=0,sticky='e')
				lbl_transports.grid(row=3,column=0,sticky='e')
				lbl_objects.grid(row=4,column=0,sticky='e')

				lbl_parent_val.grid(row=0,column=1,sticky='w')
				lbl_stories_val.grid(row=1,column=1,sticky='w')
				lbl_charms_val.grid(row=2,column=1,sticky='w')
				lbl_transports_val.grid(row=3,column=1,sticky='w')
				lbl_objects_val.grid(row=4,column=1,sticky='w')

				block.pack(fill='x',expand=True,pady=10)

		else:
			lbl_no_qry = tk.Label(self.window,text='No Results Found',font=('Arial',24))
			lbl_no_qry.pack(anchor='nw')

		self.pack(anchor='nw',side='top',fill='both',expand=True)
		self.update_idletasks()
		self.set_scroll()

	def set_scroll(self,event=None):
		''' set the scroll region based of the amount of entries '''
		bbox = self.canvas.bbox('all')
		if bbox[3] < int(self.canvas['height'])+10 and self.vscroll.winfo_exists():
			self.vscroll.pack_forget()
		else:
			if self.master.master.screen_id == self.master:
				self.vscroll.pack(side='right',anchor='e',fill='y')#grid(row=0,column=2,padx=0,sticky='ns')
		self.canvas.configure(scrollregion=bbox)

	def reset_fields(self):
		''' reset fields '''
		for item in self.window.winfo_children():
			item.destroy()

	def get_item(self,event=None):
		''' get item '''
		parent = self.validate.read_db('parent','parent',event.widget.id)[0]

		[self.master.stories.append({'parent':row[0] ,
																'story':row[1],
																'description':row[2]}) 
			for row in self.validate.read_db('story','parent',parent[0])]

		[self.master.charms.append({'parent': row[0],
																'story':row[1],
																'charm':row[2],
																'description':row[3]})
			for row in self.validate.read_db('charm','parent',parent[0])]

		[self.master.transports.append({'parent': row[0],
																		'transport':row[1],
																		'charm':row[2],
																		'description':row[3]}) 
			for row in self.validate.read_db('transport','parent',parent[0])]

		[self.master.objects.append({'parent':row[0],
																'objectId':row[1],
																'transport':row[2],
																'objectType':row[3],
																'objectName':row[4],
																'description':row[5]})
			for row in self.validate.read_db('object','parent',parent[0])]

		[self.master.files.append({'parent':row[0],
																		'objectId':row[1],
																		'objectName':row[2],
																		'transport':row[3],
																		'dFileName':row[4],
																		'dFilePath':row[5],
																		'dFileId':row[6],
																		'dFileCont':''})
			for row in self.validate.read_db('files','parent',parent[0])]



		self.pack_forget()
		self.master.parent = parent[0]
		self.master.parent_desc = parent[1]
		self.master.parent_entry.ent_parent.insert(0,parent[0])
		self.master.parent_entry.ent_descr.insert(0,parent[1])
		self.master.parent_entry.ent_parent.configure(state='disabled')
		self.master.story_records.add_story()
		self.master.change_records.set_display()
		self.master.file_records.add_file_to_view()
		self.master.object_records.add_obj_to_view()
		self.master.notes.pack(side='right',anchor='nw',pady=(25,0))
		self.master.parent_entry.pack(side='top',fill='x',expand=True,padx=10,pady=5)
		self.master.story_records.pack(after=self.master.parent_entry,fill='x',expand=True,padx=10,pady=5)
		self.master.change_records.pack(after=self.master.story_records,fill='x',expand=True,padx=10,pady=5)
		self.master.object_records.pack(after=self.master.change_records,fill='x',expand=True,padx=10,pady=5)
		self.master.file_records.pack(after=self.master.object_records,fill='x',expand=True,padx=10,pady=5)
		self.master.main_buttons.pack(after=self.master.file_records,fill='x',expand=True,padx=10,pady=5)
		self.master.main_buttons.btn_expo.grid(row=0,column=2)

		for item in self.master.notes.winfo_children():
			item.destroy()

		result = self.master.db_conn.select_table('note_header','parent',parent[0]).fetchone()
		
		for item in self.master.db_conn.select_table('notes','noteid',str(result[0])).fetchall():
			label = tk.Label(self.master.notes,text=item[1],wraplength=200,justify='left')
			label.pack(anchor='w')


		self.master.notes.configure(bd=2,relief='groove')

class ParentEntry(base.ParentEntry):
	''' parent entry '''

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
		
		self.master.delta_stories.append({'parent':self.master.parent,
																'story':story,
																'description':descr,
																'delta':'+'})

		charms = [item['charm'] for item in self.master.charms]
		if charm not in charms:
			# add new charm & transport to master list
			self.master.charms.append({'story':story,
																 'charm':charm,
																 'description':descr})

			self.master.delta_charm.append({'parent':self.master.parent,
																			'story':story,
																			'charm':charm,
																			'descr':descr,
																			'delta':'+'})

		self.master.story_records.add_story()
		self.cancel()

	def cancel(self):
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

		def add_story(self,event=None,storyId=None):
			''' add story '''
			#self.reset_fields()

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
				cbtn_sel.grid(row=0,column=0)#,padx=(5,0)
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
			self.add_story()
			#self.canvas.configure(height=50)

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
						change['delta'] = '-'
						if self.master.delta_charm:
							for n in self.master.delta_charm:
								if n['charm'] == changeId['charm']:
									n['delta'] = '-'
								else:
									self.master.delta_charm.append(change)
						else:
								self.master.delta_charm.append(change)
						self.master.charms.remove(change)

			for change in self.master.stories[:]:
				 if change['story'] == changeId['story']:
						change['delta'] = '-'
						if self.master.delta_stories:
							for n in self.master.delta_stories:
								if n['story'] == changeId['story']:
									n['delta'] = '-'
								else:
									self.master.delta_stories.append(change)
						else:
								self.master.delta_stories.append(change)
						self.master.stories.remove(change)

			[self.master.change_records.remove(event=None,changeId={'transport':change['transport']}) 
				for change in self.master.transports if change['charm'] == changeId['charm']]
			[self.master.change_records.remove(event=None,changeId={'transport':change['transport']}) 
				for change in self.master.delta_transport if change['charm'] == changeId['charm']]

			self.add_story()
			self.update_idletasks()
			self.set_scroll()
			self.sel_row = None


class ChangeEntry(base.ChangeEntry):
	''' change entry '''

	def submit(self,event):
		''' top level submit event '''
		#story = self.v_story.get()
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

			self.master.delta_transport.append({'parent': self.master.parent,
																					'transport':trans,
																					'charm':charm,
																					'description':descr,
																					'delta':'+'})

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
			cbtn_sel.grid(row=0,column=0)#,padx=(5,0)
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
					change['delta'] = '-'
					if self.master.delta_transport:
						for n in self.master.delta_transport:
							if n['transport'] == changeId['transport']:
								n['delta'] = '-'
							else:
								self.master.delta_transport.append(change)
					else:
							self.master.delta_transport.append(change)
					self.master.transports.remove(change)

		[self.master.object_records.remove_obj_from_view(event=None,objectId=obj['objectId']) 
			for obj in self.master.objects if obj['transport'] == changeId['transport']]
		[self.master.object_records.remove_obj_from_view(event=None,objectId=obj['objectId']) 
			for obj in self.master.delta_object if obj['transport'] == changeId['transport']]

		self.set_display()
		self.update_idletasks()
		self.set_scroll()
		self.sel_row = None


class ObjectRecords(base.ObjectRecords):
	''' view for session created objects '''

	def add_obj_to_view(self,objectId=None):
		''' add objects to the view '''
		self.reset_fields()
		self.master.objects.sort(key=lambda a: a['transport'])
		for item in self.master.objects:
			#if item['objectId'] == objectId:
				# self.main objects
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
			#line.pack(side='bottom')

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
		for widget in self.objects.winfo_children():
			if widget._name != 'header':
				widget.destroy()
		self.sel_row = None

	def sel_obj(self,event=None):
		''' move selected object to the entry view '''
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
		''' remove the object and file from the views, update deltas '''
		if objectId == 0:
			objectId = 0
		elif not objectId:
			objectId = self.sel_row.id
		
		# object table delta updates
		for obj in self.master.objects[:]:
			if obj['objectId'] == objectId:
				obj['delta'] = '-'
				if self.master.delta_object:
					for n in self.master.delta_object:
						if n['objectId'] == objectId:
							n['delta'] = '-'
						else:
							self.master.delta_object.append(obj)
				else:
					self.master.delta_object.append(obj)
				self.master.objects.remove(obj)
		#[self.master.objects.remove(obj) for obj in self.master.objects if obj['objectId'] == objectId]
		self.master.file_records.remove_file(event=None,objectId=objectId)

		#	# file table delta updates
		#	for file in self.master.files:
		#		 if file['objectId'] == objectId:
		#				file['delta'] = '-'
		#				self.master.delta_files.append(file)
		#	[self.master.files.remove(file) for file in self.master.files if file['objectId'] == objectId]
#
		#self.master.file_records.add_file_to_view()

		self.add_obj_to_view()
		self.update_idletasks()
		self.set_scroll()
		self.sel_row = None

	def edit_entry(self,event=None):
		''' edit entry '''
		if self.sel_row.id or self.sel_row.id == 0:
			self.master.object_entry.new_object()
			self.master.object_entry.grab_set()
			for item in self.objects.winfo_children():
				if item._name != 'header':
					if item.id == self.sel_row.id:
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


class ObjectEntry(base.ObjectEntry):
	''' object data entry '''

	def add_obj(self,event=None):
		''' add object '''
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
					for item in self.master.objects:
						if item['objectId'] == objectId:
							alert = messagebox.askyesno('Warning','Overwrite Entry?')
							if alert == True:
								item['transport'] = transport
								item['objectType'] = objectType
								item['objectName'] = objectName
								item['description'] = description

							# update delta (*)
								delta = '*'
								if self.master.delta_object:
									for row in self.master.delta_object:
										if row['objectId'] == item['objectId'] and row['delta'] != '+':
											if self.master.db_conn.select_table('object','object_id',str(row['objectId'])).fetchone():
												delta = '*'
											else:
												delta = '+'
										else:
											delta = '+'
											self.master.delta_object.remove(row)

								self.master.delta_object.append({'parent': self.master.parent,
																								'objectId':item['objectId'],
																								 'transport':transport,
																								 'objectType':objectType,
																								 'objectName':objectName,
																								 'description':description,
																								 'delta':'{}'.format(delta)})
								for file in self.master.files:
									if objectId == file['objectId']:
										file['transport'] = transport
										file['objectName'] = objectName

								# update delta (*)
								delta = '*'
								if self.master.delta_files:
									for row in self.master.delta_files:
										if row['objectId'] == objectId and row['delta'] != '+':
											if self.master.db_conn.select_table('files','object_id',str(row['objectId'])).fetchone():
												row['delta'] = '*'
											else:
												row['delta'] = '+'
										else:
											row['delta'] = '+'
								else:
									for file in self.master.files:
										if file['objectId'] == objectId:
											self.master.delta_files.append(file)
											file['delta'] = '*'

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

			# update delta (+)
			self.master.delta_object.append({'parent': self.master.parent,
																			 'objectId':self.object_id,
																			 'transport':transport,
																			 'objectType':objectType,
																			 'objectName':objectName,
																			 'description':description,
																			 'delta':'+'})

			# create the object table and add new object to view
			#if not self.master.object_records.grid():
				#self.master.object_records.grid(row=4,padx=10,pady=5,sticky='w')
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

	def new_object(self,event=None):
		''' new object '''
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


class FileEntry(base.FileEntry):
	''' file entry '''

	def submit(self,event):
		''' submit '''
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

			self.master.delta_files.append({'parent':self.master.parent,
																			'objectId':self.objectId,
																			'objectName':self.objectName,
																			'transport':self.transport,
																			'dFileName':self.dfile_name,
																			'dFilePath':self.dfile_file,
																			'dFileId':self.dfile_id,
																			'dFileCont':self.dfile_cont,
																			'delta':'+'})

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
		''' select '''
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
		''' cancel '''
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

	def attach_file(self,event=None):
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

				cbtn_sel.id,  cbtn_sel.name  = item['objectId'], item['dFileName']
				#lbl_fname.id, lbl_fname.name = item['objectId'], item['dFileName']
				#lbl_obj.id,   lbl_obj.name   = item['objectId'], item['dFileName']
				#lbl_tran.id,  lbl_tran.name  = item['objectId'], item['dFileName']

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
		''' select file '''
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

	def remove_file(self,event=None,objectId=None):
		''' remove file '''
		if objectId or objectId == 0:

			# file table delta updates
			for file in self.master.files[:]:
				if file['objectId'] == objectId:
					self.master.files.remove
					file['delta'] = '-'
					if self.master.delta_files:
						for n in self.master.delta_files:
							if n['objectId'] == objectId and n['dFileName'] == file['dFileName']:
								n['delta'] = '-'
							else:
								self.master.delta_files.append(file)
					else:
						self.master.delta_files.append(file)
					self.master.files.remove(file)

		else:
			objectId = self.sel_row.id
			fileName = self.sel_row.name
			# remove item from view, then from the master file list
			for file in self.master.files[:]:
				if file['objectId'] == objectId and file['dFileName'] == fileName:
					file['delta'] = '-'
					if self.master.delta_object:
						for n in self.master.delta_files:
							if n['objectId'] == objectId:
								n['delta'] = '-'
							else:
								self.master.delta_files.append(file)
					else:
						self.master.delta_object.append(file)
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

	def canc_log(self,event=None):
		''' cancel log '''
		self.master.parent = ''
		self.master.stories.clear()
		self.master.charms.clear()
		self.master.objects.clear()
		self.master.files.clear()
		self.master.transports.clear()
		self.master.delta_parent.clear()
		self.master.delta_object.clear()
		self.master.delta_files.clear()
		self.master.delta_transport.clear()
		self.master.delta_charm.clear()
		self.master.notes.pack_forget()
		self.master.parent_entry.pack_forget()
		self.master.story_records.pack_forget()
		self.master.file_records.pack_forget()
		self.master.main_buttons.pack_forget()
		self.master.change_records.pack_forget()
		self.master.object_records.pack_forget()
		self.master.parent_entry.reset_fields()
		self.master.story_records.reset_fields()
		self.master.change_records.reset_fields()
		self.master.object_records.reset_fields()
		self.master.object_entry.reset_fields()
		self.master.file_records.reset_fields()
		self.master.file_entry.wm_withdraw()
		self.master.change_entry.wm_withdraw()
		self.master.object_entry.wm_withdraw()

	def cancel(self,event=None):
		''' cancel '''
		self.canc_log()
		self.master.pack_forget()
		self._root().notes.pack(fill='both',expand=True,pady=(10,0))
		self._root().screen_id = self._root().notes

	def save_log(self,event=None):
		''' save log '''
		# add logic for updating story table
		if True == True:
		#if self.master.validation.validate_parent_data(self.ent_parent.get(),
		#																								self.ent_story.get(),
		#																								self.ent_p_descr.get()):
			
			if self.master.parent_entry.ent_descr != self.master.parent_desc:
				self.master.delta_parent.clear()
				self.master.delta_parent.append({'parent':self.master.parent,
																				 'descr':self.master.parent_entry.ent_descr.get()})
			story = None
			description = None
			descriptions = [story['description'] for story in self.master.stories]

			# get a list of stories that have been entered, add to master list
			self.master.stories.clear()
			for item in self.master.story_records.window.winfo_children():
				if '!frame' in str(item):
					for i in item.winfo_children():
						if '!label' in str(i):
							if i.name == 'story':
								story = i['text']
							if i.name == 'descr':
								description = i['text']
						elif '!button' in str(i):
							i.destroy()
					self.master.stories.append({'parent':self.master.parent,
																			'story':story,
																			'description':description})
					if self.master.db_conn.select_table('story','story',story).fetchone():
						if description not in descriptions:
							for item in self.master.delta_stories:
								if item['story'] == story:
									del self.master.delta_stories[self.master.delta_stories.index(item)]
							self.master.delta_stories.append({'parent':self.master.parent,
																								'story':story,
																								'description':description,
																								'delta':'*'})
					else:
						for item in self.master.delta_stories:
							if item['story'] == story:
								del self.master.delta_stories[self.master.delta_stories.index(item)]
						self.master.delta_stories.append({'parent':self.master.parent,
																							'story':story,
																							'description':description,
																							'delta':'+'})

		# validate no unsaved data
		if self.master.object_entry.ent_obj.get():
			error = True
			for item in self.master.objects:
				if item['objectName'] == self.master.object_entry.ent_obj.get():
					error = False

			if error:
				alert = messagebox.showerror('error','Save or cancel object before moving on')
				return

		parent = [list(item.values()) for item in self.master.delta_parent]
		if parent:
			for item in parent:
				result = self.master.db_conn.update_table('parent','descr',item[1],'parent',item[0])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# check if file already exists w/reference to key fields
		for row in self.master.delta_files:
			if row['delta'] == '+':
				file = row['dFilePath']
				try:
					file.touch(exist_ok=False)
				except(FileExistsError):
					alert = messagebox.showerror('Error','Error saving file!')
					return

				# write contents to new file
				with file.open(mode='w',encoding='utf-8') as ofile:
					ofile.write(row['dFileCont'])
			elif row['delta'] == '-':
				file = pathlib.Path(row['dFilePath'])
				try:
					file.unlink()
				except(FileNotFoundError):
					alert = messagebox.showerror('Error','Error deleting file!')
					return

		# change win path to string, remove file content
		for item in self.master.delta_files:
			item['dFilePath'] = str(item['dFilePath'])

		# update files table
		files_add = [list(item.values()) for item in self.master.delta_files if item['delta'] == '+']
		files_del = [item['dFilePath'] for item in self.master.delta_files if item['delta'] == '-']

		if files_add:
			for item in files_add:
				result = self.master.db_conn.insert_table('files',item[0:7])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if files_del:
			for item in files_del:
				result = self.master.db_conn.delete_table('files','file_path',item)
				if result:
					alert = messagebox.showerror('Error',result)
					return

		story_add = [list(item.values()) for item in self.master.delta_stories if item['delta'] == '+']
		#story_mod = [list(item.values()) for item in self.master.delta_stories if item['delta'] == '*']
		story_del = [list(item.values()) for item in self.master.delta_stories if item['delta'] == '-']

		if story_add:
			for row in story_add:
				result = self.master.db_conn.insert_table('story',row[0:3])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if story_del:
			for row in story_del:
				result = self.master.db_conn.delete_table('story','story',row[1])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update charm table
		charm_add = [list(item.values()) for item in self.master.delta_charm if item['delta'] == '+']
		charm_del = [list(item.values()) for item in self.master.delta_charm if item['delta'] == '-']

		if charm_add:
			for item in charm_add:
				result = self.master.db_conn.insert_table('charm',item[0:4])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if charm_del:
			for item in charm_del:
				result = self.master.db_conn.delete_table('charm','charm',item[2])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update transport table
		transport_add = [list(item.values()) for item in self.master.delta_transport if item['delta'] == '+']
		transport_del = [list(item.values()) for item in self.master.delta_transport if item['delta'] == '-']

		if transport_add:
			for item in transport_add:
				result = self.master.db_conn.insert_table('transport',item[0:4])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if transport_del:
			for item in transport_del:
				result = self.master.db_conn.delete_table('transport','transport',item[1])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update object table
		object_add = [list(item.values()) for item in self.master.delta_object if item['delta'] == '+']
		object_del = [list(item.values()) for item in self.master.delta_object if item['delta'] == '-']
		object_mod = [list(item.values()) for item in self.master.delta_object if item['delta'] == '*']

		if object_add:
			for row in object_add:
				result = self.master.db_conn.insert_table('object',row[0:6])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if object_del:
			for row in object_del:
				result = self.master.db_conn.delete_table('object','object_id',row[1])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if object_mod:
			for row in object_mod:
				result = self.master.db_conn.update_table('object','transport',row[2],'object_id',row[1])
				result = self.master.db_conn.update_table('object','object_type',row[3],'object_id',row[1])
				result = self.master.db_conn.update_table('object','object_name',row[4],'object_id',row[1])
				result = self.master.db_conn.update_table('object','descr',row[5],'object_id',row[1])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		alert = messagebox.showinfo('Success','Log Successfully Updated')
		self.master.delta_object.clear()
		self.master.delta_files.clear()
		self.master.delta_charm.clear()
		self.master.delta_transport.clear()

	def export_log(self,event=None):
		''' export log '''
		if not self.master.delta_parent\
				and not self.master.delta_stories\
				and not self.master.delta_charm\
				and not self.master.delta_transport\
				and not self.master.delta_object\
				and not self.master.delta_files:
			master_log = self.create_master_log()
			parent = str(self.master.parent)
			pdesc = str(self.master.parent_desc)
			directory = '(Log) {} - {}'.format(parent,pdesc)
			path = pathlib.Path(askdirectory()+'\\{}'.format(directory))
			if path:
				path.mkdir()
				master_des = path.joinpath(pathlib.Path('mainlog'))
				master_des.touch(exist_ok=False)
				master_des.write_text(master_log)
				for item in self.master.files:
					src_file = pathlib.Path(item['dFilePath'])
					des_file = path.joinpath(pathlib.Path(item['dFileName']))
					des_file.touch(exist_ok=False)
					with src_file.open() as file:
						text = file.read()
						des_file.write_text(text)
		alert = messagebox.showinfo('Success','Log Successfully Exported!')
		return

	def create_master_log(self):
		''' create master log '''
		parent = self.master.parent
		pdesc = self.master.parent_desc
		text = '''PARENT: {} - {}\n\n'''.format(parent,pdesc)
		for story in self.master.stories:
			text = text + 'STORY: {}\n'.format(story['story'])
			for charm in self.master.charms:
				if story['story'] == charm['story']:
					text = text + 'CHARM: {} - {}\n'.format(charm['charm'],charm['description'])
					for trans in self.master.transports:
						if charm['charm'] == trans['charm']:
							text = text + 'TRANSPORT: {}'.format(trans['transport']) +'\n'
							for obj in self.master.objects:
								if obj['transport'] == trans['transport']:
									text = text+'Object Name: {}\nObject Type: {}\nDescription:\n{}\nAttachments:\n'.format(obj['objectName'],obj['objectType'],obj['description'])
									for file in self.master.files:
										if obj['objectId'] == file['objectId']:
											text = text+'{}\n'.format(file['dFileName'])
									text = text + '\n'
		return text
					
