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

		# maintain connection to DB from master
		self.db_conn = self.master.db_conn

		# screen objects
		self.search_options = SearchOptions(self)
		self.parent_entry   = ParentEntry(self)
		self.parent_records = ParentRecords(self)
		self.change_entry   = ChangeEntry(self)
		self.change_records = ChangeRecords(self)
		self.object_entry   = ObjectEntry(self)
		self.object_records = ObjectRecords(self)
		self.file_entry     = FileEntry(self)
		self.file_records   = FileRecords(self)
		self.main_buttons   = MainButtons(self)
		self.validation     = self.master.validation

		# set the initial display
		self.search_options.grid(row=0,padx=10,pady=5,sticky='w')

	def reset(self):
		''' reset the screen to initial settings '''
		self.main_buttons.canc_log()


class SearchOptions(base.SearchOptions):
	''' selection options for searching '''

	def search(self,event):
		''' select from the database and display to user '''
		self.master.reset()
		qry_parent = None
		
		# get selections
		if self.ent_parent.get():
			qry_parent = self.master.db_conn.select_table('parent','parent',self.ent_parent.get()).fetchone()
			if qry_parent:
				qry_story = self.master.db_conn.select_table('story','parent',qry_parent[0]).fetchall()
				if qry_story:
					for story in qry_story:
						self.master.stories.append({'parent':qry_parent[0],
																				'story':story[1],
																				'description':story[2]})
						qry_charm = self.master.db_conn.select_table('charm','story',story[1]).fetchall()
						if qry_charm:
							for charm in qry_charm:
								self.master.charms.append({'story':charm[1],
																					'charm':charm[2],
																					'description':charm[3]})
								qry_transport = self.master.db_conn.select_table('transport','charm',charm[2]).fetchall()
								if qry_transport:
									for tran in qry_transport:
										#qry = self.master.db_conn.select_table('charm','charm',tran[1]).fetchone()
										self.master.transports.append({'story':story[1],
																									 'transport':tran[0],
																									 'charm':tran[1],
																									 'description':tran[2]})
										qry_object = self.master.db_conn.select_table('object','transport',tran[0]).fetchall()
										if qry_object:
											for obj in qry_object:
												self.master.objects.append({'objectId':obj[0],
																										'transport':obj[1],
																										'objectType':obj[2],
																										'objectName':obj[3],
																										'description':obj[4]})
		elif self.ent_story.get():
			qry_story = self.master.db_conn.select_table('story','story',self.ent_story.get()).fetchone()
			if qry_story:
				qry_parent = [qry_story[0]]
				self.master.stories.append({'parent':qry_parent[0],
																		'story':qry_story[1],
																		'description':qry_story[2]})
				qry_charm = self.master.db_conn.select_table('charm','story',qry_story[1]).fetchall()
				if qry_charm:
					for charm in qry_charm:
						self.master.charms.append({'story':charm[1],
																			'charm':charm[2],
																			'description':charm[3]})
						qry_transport = self.master.db_conn.select_table('transport','charm',charm[2]).fetchall()
						if qry_transport:
							for tran in qry_transport:
								self.master.transports.append({'story':qry_story[1],
																							 'transport':tran[0],
																							 'charm':tran[1],
																							 'description':tran[2]})
								qry_object = self.master.db_conn.select_table('object','transport',tran[0]).fetchall()
								if qry_object:
									for obj in qry_object:
										self.master.objects.append({'objectId':obj[0],
																								'transport':obj[1],
																								'objectType':obj[2],
																								'objectName':obj[3],
																								'description':obj[4]})
		elif self.ent_charm.get():
			qry_charm = self.master.db_conn.select_table('charm','charm',self.ent_charm.get()).fetchone()
			if qry_charm:
				self.master.charms.append({'story':qry_charm[1],
																	'charm':qry_charm[2],
																	'description':qry_charm[3]})
				qry_story = self.master.db_conn.select_table('story','story',qry_charm[1]).fetchone()
				if qry_story:
					qry_parent = [qry_story[0]]
					self.master.stories.append({'parent':qry_story[0],
																			'story':qry_story[1],
																			'description':qry_story[2]})
					qry_transport = self.master.db_conn.select_table('transport','charm',qry_charm[2]).fetchall()
					if qry_transport:
						for tran in qry_transport:
							self.master.transports.append({'story':qry_story[1],
																						 'transport':tran[0],
																						 'charm':tran[1],
																						 'description':tran[2]})
							qry_object = self.master.db_conn.select_table('object','transport',tran[0]).fetchall()
							if qry_object:
								for obj in qry_object:
									self.master.objects.append({'objectId':obj[0],
																							'transport':obj[1],
																							'objectType':obj[2],
																							'objectName':obj[3],
																							'description':obj[4]})

		elif self.ent_desc.get():
			pass
		elif self.ent_tran.get():
			qry_transport = self.master.db_conn.select_table('transport','transport',self.ent_tran.get()).fetchone()
			if qry_transport:
				qry = self.master.db_conn.select_table('charm','charm',qry_transport[1]).fetchone()
				self.master.transports.append({'story':qry[1],
																	 		'transport':qry_transport[0],
														 					'charm':qry_transport[1],
														 					'description':qry_transport[2]})
				qry_charm = self.master.db_conn.select_table('charm','charm',qry_transport[1]).fetchone()
				if qry_charm:
					self.master.charms.append({'story':qry_charm[1],
																		 'charm':qry_charm[2],
																		 'description':qry_charm[3]})
					qry_story = self.master.db_conn.select_table('story','story',qry_charm[1]).fetchone()
					if qry_story:
						self.master.stories.append({'parent':qry_story[0],
																				'story':qry_story[1],
																				'description':qry_story[2]})
						qry_parent = [qry_story[0]]
						qry_object = self.master.db_conn.select_table('object','transport',qry_transport[0]).fetchall()
						if qry_object:
							for obj in qry_object:
								self.master.objects.append({'objectId':obj[0],
																						'transport':obj[1],
																						'objectType':obj[2],
																						'objectName':obj[3],
																						'description':obj[4]})
		elif self.ent_obj.get():
			pass
		elif self.ent_objty.get():
			pass

		# set the parent & story
		if qry_parent:
			self.master.parent = qry_parent[0]
			self.master.parent_desc = qry_parent[1]
			# hide the search fields
			self.main.grid_forget()
			self.btn_search.configure(state='disabled')
			self.btn_search.unbind('<Button-1>')
		else:
			alert = messagebox.showerror('Error','No record found.')
			return

		# set the parent & story to be displayed
		self.master.parent_records.ent_parent.insert(0,self.master.parent)
		self.master.parent_records.ent_parent.configure(state='disabled')
		self.master.parent_records.ent_p_descr.insert(0,self.master.parent_desc)

		if self.master.objects:
			for item in self.master.objects:
				self.master.object_records.add_obj_to_view()

		# get files
		for item in self.master.objects:
			qry_files = self.master.db_conn.select_table('files','object_id',str(item['objectId'])).fetchall()
			if qry_files:
				for row in qry_files:
					self.master.files.append({'objectId':row[0],
																		'objectName':row[1],
																		'transport':row[2],
																		'dFileName':row[3],
																		'dFilePath':row[4],
																		'dFileId':row[5],
																		'dFileCont':''})

		# set the display
		self.master.parent_records.add_story()
		self.master.change_records.set_display()
		self.master.file_records.add_file_to_view()
		self.master.parent_records.grid(row=1,padx=10,pady=5,sticky='w')
		self.master.change_records.grid(row=2,padx=10,pady=5,sticky='w')
		self.master.object_records.grid(row=3,padx=10,pady=5,sticky='w')
		self.master.file_records.grid(row=4,padx=10,pady=5,sticky='w')
		self.master.main_buttons.grid(row=5,padx=10,pady=5,sticky='w')
		self.master.main_buttons.btn_expo.grid(row=0,column=2)
		
	def reset_fields(self,event=None):
		''' reset the screen '''
		self.master.reset()
		self.main.grid(row=1,sticky='nsew')
		self.btn_search.configure(state='normal')
		self.btn_search.bind('<Button-1>',self.search)
		self.ent_parent.focus_set()
		for item in self.main.winfo_children():
			if item.winfo_class() == 'Entry':
				item.delete(0,'end')


class ParentEntry(base.ParentEntry):
	''' change entry '''

	def submit(self,event=None):
		''' submit button event handler '''
		story = self.ent_story.get()
		descr = self.ent_descr.get()

		self.master.stories.append({'parent':self.master.parent,
																'story':story,
																'description':descr})
		
		self.master.delta_stories.append({'parent':self.master.parent,
																'story':story,
																'description':descr,
																'delta':'+'})

		self.master.parent_records.add_story()
		self.cancel()

	def cancel(self):
		''' cancel '''
		self.ent_story.delete(0,'end')
		self.ent_descr.delete(0,'end')
		self.wm_withdraw()

	def new_story(self):
		''' new story '''
		x = self._root().winfo_x()
		y = self._root().winfo_y()
		self.geometry("+%d+%d" %(x+200,y+200))
		self.wm_deiconify()


class ParentRecords(base.ParentRecords):
		''' change entry data '''

		def new_story(self,event=None):
			''' new story '''
			self.master.parent_entry.new_story()

		def add_story(self,event=None,storyId=None):
			''' add story '''
			for item in self.window.winfo_children():
				item.destroy()

			for item in self.master.stories:
				# row for table
				row = tk.Frame(self.window)

				# story & description
				lbl_story = tk.Label(row,text=item['story'],width=10,anchor='w')
				lbl_descr = tk.Label(row,text=item['description'],width=40,anchor='w')

				# config
				lbl_story.name = 'story'
				lbl_descr.name = 'descr'
				row.id = self.row_index

				# grid
				row.grid(row=self.row_index,column=0,pady=(2,0),sticky='w')
				lbl_story.grid(row=0,column=0,padx=(5,0))
				lbl_descr.grid(row=0,column=1)

				self.row_index = self.row_index + 1

			#if 'Configure' not in str(event):
				#self.canvas.configure(height=95)
			self.update_idletasks()
			self.set_scroll()
			self.canvas.unbind('<Configure>')

		def reset_fields(self):
			''' reset fields '''
			self.row_index = 0
			self.ent_parent.configure(state='normal')
			self.ent_parent.delete(0,'end')
			self.ent_p_descr.delete(0,'end')
			self.ent_parent.focus_set()
			for item in self.window.winfo_children():
				item.destroy()
			self.add_story()
			self.canvas.configure(height=50)

		def modify_display(self,event=None):
			''' modify display '''
			# validate fields are filled & follow naming conv.
			if True == True:
			#if self.master.validation.validate_parent_data(self.ent_parent.get(),
			#																								self.ent_story.get(),
			#																								self.ent_p_descr.get()):
				self.ent_parent.configure(state='disabled')
				if self.ent_p_descr != self.master.parent_desc:
					self.master.delta_parent.clear()
					self.master.delta_parent.append({'parent':self.master.parent,
																					 'descr':self.ent_p_descr.get()})
				story = None
				description = None
				descriptions = [story['description'] for story in self.master.stories]

				# get a list of stories that have been entered, add to master list
				self.master.stories.clear()
				for item in self.window.winfo_children():
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

		def set_scroll(self,event=None):
			''' set the scroll region based of the amount of entries '''
			bbox = self.canvas.bbox('all')
			if bbox[3] < int(self.canvas['height'])+10 and self.vscroll.winfo_exists():
				self.vscroll.grid_forget()
			else:
				if self.master.master.screen_id == self.master:
					self.vscroll.grid(row=0,column=1,sticky='ns')
			self.canvas.configure(scrollregion=bbox)


class ChangeEntry(base.ChangeEntry):
	''' change entry '''

	def submit(self,event):
		''' top level submit event '''
		story = self.v_story.get()
		charm = self.ent_charm.get()
		trans = self.ent_trans.get()
		descr = self.ent_descr.get()

		for item in self.master.transports:
			if item['transport'] == trans:
				alert = messagebox.showerror('Error','Transport already created in session!')
				return

		if True == True:
		#if self.master.validation.validate_charm_and_tran(charm,trans,descr):

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

			self.master.transports.append({'story':story,
																		 'transport':trans,
																		 'charm':charm,
																		 'description':descr})

			self.master.delta_transport.append({'transport':trans,
																					 'charm':charm,
																					 'description':descr,
																					 'delta':'+'})

			self.cancel()
			self.master.change_records.set_display()

	def cancel(self,event=None):
		''' top cancel '''
		self.wm_withdraw()
		self.v_story.set('Select a Story')
		self.ent_charm.delete(0,'end')
		self.ent_trans.delete(0,'end')
		self.ent_descr.delete(0,'end')

	def new_change(self):
		''' new change '''
		stories = [item['story'] for item in self.master.stories]
		self.opt_story['menu'].delete(0,'end')
		for item in stories:
			self.opt_story['menu'].add_command(label=item,command=tk._setit(self.v_story,item))
		x = self._root().winfo_x()
		y = self._root().winfo_y()
		self.geometry("+%d+%d" %(x+200,y+200))
		self.wm_deiconify()


class ChangeRecords(base.ChangeRecords):
	''' view for charm records '''

	def add(self,event):
		''' add charm & transport '''
		self.master.change_entry.new_change()

	def remove(self,event):
		''' remove charm & transport '''
		pass

	def set_scroll(self,event=None):
		''' set the scroll region based of the amount of entries '''
		bbox = self.canvas.bbox('all')
		if bbox[3] < int(self.canvas['height'])+10 and self.vscroll.winfo_exists():
			self.vscroll.grid_forget()
		else:
			if self.master.master.screen_id == self.master:
				self.vscroll.grid(row=2,column=1,sticky='ns')
		self.canvas.configure(scrollregion=bbox)

	def set_display(self):
		''' add items to the parent and charm/transport view '''
		self.reset_fields()
		for item in self.master.transports:
			lbl_story = tk.Label(self.charms,anchor='w',width=10,text=item['story'])
			lbl_charm = tk.Label(self.charms,anchor='w',width=10,text=item['charm'])
			lbl_trans = tk.Label(self.charms,anchor='w',width=10,text=item['transport'])
			lbl_descr = tk.Label(self.charms,anchor='w',width=40,text=item['description'])
			lbl_story.grid(row=self.row_index,column=0,padx=5)
			lbl_charm.grid(row=self.row_index,column=1,padx=5)
			lbl_trans.grid(row=self.row_index,column=2,padx=5)
			lbl_descr.grid(row=self.row_index,column=3,padx=5)

			self.row_index = self.row_index + 1

		# update the scrollregion
		self.update_idletasks()
		self.set_scroll()
		
	def reset_fields(self):
		''' reset the data '''
		for item in self.charms.winfo_children():
			item.destroy()


class ObjectRecords(base.ObjectRecords):
	''' view for session created objects '''

	def add_obj_to_view(self,objectId=None):
		''' add objects to the view '''
		self.reset_fields()
		for item in self.master.objects:
			#if item['objectId'] == objectId:
				# self.main objects
			line = tk.Frame(self.main)
			line.id = item['objectId']
			cbtn_sel   = tk.Checkbutton(line,width=1,height=1,anchor='w',text=' ')
			lbl_tran  = tk.Label(line,width=15,anchor='w',text=item['transport'])
			lbl_objty = tk.Label(line,width=15,anchor='w',text=item['objectType'])
			lbl_obj   = tk.Label(line,width=40,anchor='w',text=item['objectName'])
			lbl_desc  = tk.Label(line,width=25,anchor='w',text=item['description'].strip('\n'))

			# config
			cbtn_sel.sel = tk.StringVar()
			cbtn_sel.configure(variable=cbtn_sel.sel)
			cbtn_sel.sel.set(0)

			# set an index for table row reference
			cbtn_sel.id,  cbtn_sel.name  = item['objectId'],'sel'
			lbl_tran.id,  lbl_tran.name  = item['objectId'],'transport'
			lbl_objty.id, lbl_objty.name = item['objectId'],'objectType'
			lbl_obj.id,   lbl_obj.name   = item['objectId'],'objectName'
			lbl_desc.id,  lbl_desc.name  = item['objectId'],'description'

			# bind button one click event for selecting table row
			cbtn_sel.bind('<ButtonRelease-1>',self.sel_obj)

			# grid placement
			cbtn_sel.grid(row=0,column=0)
			lbl_tran.grid(row=0,column=1)
			lbl_objty.grid(row=0,column=2)
			lbl_obj.grid(row=0,column=3)
			lbl_desc.grid(row=0,column=4)

			line.grid(row=self.row_index)

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
		for widget in self.main.winfo_children():
			widget.destroy()	

	def sel_obj(self,event=None):
		''' move selected object to the entry view '''
		if self.sel_row.id == event.widget.id:
			self.sel_row = None
		else:
			self.sel_row = event.widget
		for item in self.main.winfo_children():
			for row in item.winfo_children():
				if '!checkbutton' in str(row):
					if event.widget.id != row.id:
						row.deselect()

	def remove_obj_from_view(self,objectId):
		''' remove the object and file from the views, update deltas '''
		objectId = self.master.object_records.sel_row.id
		if objectId or objectId == 0:

			# object table delta updates
			for obj in self.master.objects:
				 if obj['objectId'] == objectId:
						obj['delta'] = '-'
						if self.master.delta_object:
							for n in self.master.delta_object:
								if n['objectId'] == objectId:
									n['delta'] = '-'
						else:
								self.master.delta_object.append(obj)

			[self.master.objects.remove(obj) for obj in self.master.objects if obj['objectId'] == objectId]

			# file table delta updates
			for file in self.master.files:
				 if file['objectId'] == objectId:
						obj['delta'] = '-'
						self.master.delta_object.append(obj)
			[self.master.files.remove(file) for file in self.master.files if file['objectId'] == objectId]

		self.master.file_records.add_file_to_view()
		self.add_obj_to_view()
		self.update_idletasks()
		self.set_scroll()

	def set_scroll(self,event=None):
		''' set the scroll region based of the amount of entries '''
		bbox = self.canvas.bbox('all')
		if bbox[3] < int(self.canvas['height'])+10 and self.vscroll.winfo_exists():
			self.vscroll.grid_forget()
		else:
			if self.master.master.screen_id == self.master:
				self.vscroll.grid(row=1,column=1,sticky='ns')
		self.canvas.configure(scrollregion=bbox)

	def edit_entry(self,event=None):
		''' edit entry '''
		if self.sel_row.id or self.sel_row.id == 0:
			self.master.object_entry.new_object()
			self.master.object_entry.grab_set()
			for item in self.main.winfo_children():
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
		transport = self.v_trans.get()
		objectType = self.v_objty.get()
		objectName = self.ent_obj.get()
		description = self.txt_desc.get(1.0,'end')

		if True == True:
		#if self.master.validation.validate_obj_data(transport,
		#																						 objectType,
		#																						 objectName,
		#																						 description):
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

							self.master.delta_object.append({'objectId':item['objectId'],
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
			self.master.objects.append({'objectId':self.object_id,
																	'transport':transport,
																	'objectType':objectType,
																	'objectName':objectName,
																	'description':description})

			# update delta (+)
			self.master.delta_object.append({'objectId':self.object_id,
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
			self.master.files.append({'objectId':self.objectId,
																'objectName':self.objectName,
																'transport':self.transport,
																'dFileName':self.dfile_name,
																'dFilePath':self.dfile_file,
																'dFileId':self.dfile_id,
																'dFileCont':self.dfile_cont})

			self.master.delta_files.append({'objectId':self.objectId,
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
		self.objectName = self.v_object.get()
		self.transport = self.v_transport.get()
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
		self.opt_trans['menu'].delete(0,'end')
		transports = [item['transport'] for item in self.master.transports]
		for item in transports:
			self.opt_trans['menu'].add_command(label=item,command=tk._setit(self.v_transport, item))

		x = self._root().winfo_x()
		y = self._root().winfo_y()
		self.geometry("+%d+%d" %(x+200,y+200))
		self.wm_deiconify()

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
				line = tk.Frame(self.main)
				cbtn_sel = tk.Checkbutton(line,width=1,height=1,state='normal',anchor='w')
				lbl_fname = tk.Label(master=line,width=25,height=1,anchor='w',text=item['dFileName'])
				lbl_obj   = tk.Label(master=line,width=20,height=1,anchor='w',text=item['objectName'])
				lbl_tran  = tk.Label(master=line,width=20,height=1,anchor='w',text=item['transport'])

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
				lbl_fname.grid(row=0,column=1)
				lbl_obj.grid(row=0,column=2)
				lbl_tran.grid(row=0,column=3)

				line.grid(row=self.row_index,column=0)

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

		for item in self.main.winfo_children():
			for row in item.winfo_children():
				if '!checkbutton' in str(row):
					if self.sel_row:
						if self.sel_row.id == row.id and self.sel_row.name == row.name:
							pass
						else:
							row.deselect()

	def remove_file(self,objectId=None,event=None):
		''' remove file '''
		objectId = self.sel_row.id
		fileName = self.sel_row.name
		if objectId or objectId == 0:

			# remove item from view, then from the master file list
			for file in self.master.files:
				if file['objectId'] == objectId and file['dFileName'] == fileName:
					file['delta'] = '-'
					self.master.delta_files.append(file)
			[self.master.files.remove(file) for file in self.master.files if file['objectId'] == objectId and file['dFileName'] == fileName]
			#[child.destroy() for child in self.main.winfo_children() if child.id == item.id and child.name == item.name]

		# update scrollregion
		self.sel_row = None
		self.add_file_to_view()
		self.update_idletasks()
		self.set_scroll()

	def reset_fields(self):
		''' reset fields '''
		for widget in self.main.winfo_children():
			widget.destroy()

	def set_scroll(self,event=None):
		''' set the scroll region based of the amount of entries '''
		bbox = self.canvas.bbox('all')
		if bbox[3] < int(self.canvas['height'])+10 and self.vscroll.winfo_exists():
			self.vscroll.grid_forget()
		else:
			if self.master.master.screen_id == self.master:
				self.vscroll.grid(row=1,column=1,sticky='ns')
		self.canvas.configure(scrollregion=bbox)


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
		self.master.parent_records.grid_remove()
		self.master.file_records.grid_remove()
		self.master.main_buttons.grid_remove()
		self.master.change_records.grid_remove()
		self.master.object_records.grid_remove()
		self.master.change_records.reset_fields()
		self.master.object_records.reset_fields()
		self.master.object_entry.reset_fields()
		self.master.file_records.reset_fields()
		self.master.file_entry.wm_withdraw()
		self.master.change_entry.wm_withdraw()
		self.master.object_entry.wm_withdraw()

	def save_log(self,event=None):
		''' save log '''
		# add logic for updating story table

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
			file = row['dFilePath']
			if row['delta'] == '+':
				try:
					file.touch(exist_ok=False)
				except(FileExistsError):
					alert = messagebox.showerror('Error','Error saving file!')
					return

				# write contents to new file
				with file.open(mode='w',encoding='utf-8') as ofile:
					ofile.write(row['dFileCont'])

		# change win path to string, remove file content
		for item in self.master.delta_files:
			item['dFilePath'] = str(item['dFilePath'])

		# update files table
		files_add = [list(item.values()) for item in self.master.delta_files if item['delta'] == '+']
		files_del = [item['dFilePath'] for item in self.master.delta_files if item['delta'] == '-']

		if files_add:
			for item in files_add:
				result = self.master.db_conn.insert_table('files',item[0:6])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if files_del:
			for item in files_del:
				result = self.master.db_conn.delete_table('files','file_path',item)
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update charm table
		charm_add = [list(item.values()) for item in self.master.delta_charm if item['delta'] == '+']
		print(charm_add)
		if charm_add:
			for item in charm_add:
				result = self.master.db_conn.insert_table('charm',item[0:4])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update transport table
		transport_add = [list(item.values()) for item in self.master.delta_transport if item['delta'] == '+']

		if transport_add:
			for item in transport_add:
				result = self.master.db_conn.insert_table('transport',item[0:3])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		# update object table
		object_add = [list(item.values()) for item in self.master.delta_object if item['delta'] == '+']
		object_del = [list(item.values()) for item in self.master.delta_object if item['delta'] == '-']
		object_mod = [list(item.values()) for item in self.master.delta_object if item['delta'] == '*']

		if object_add:
			for row in object_add:
				result = self.master.db_conn.insert_table('object',row[0:5])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if object_del:
			for row in object_del:
				result = self.master.db_conn.delete_table('object','object_id',row[0])
				if result:
					alert = messagebox.showerror('Error',result)
					return

		if object_mod:
			for row in object_mod:
				result = self.master.db_conn.update_table('object','transport',row[1],'object_id',row[0])
				result = self.master.db_conn.update_table('object','object_type',row[2],'object_id',row[0])
				result = self.master.db_conn.update_table('object','object_name',row[3],'object_id',row[0])
				result = self.master.db_conn.update_table('object','descr',row[4],'object_id',row[0])
				if result:
					alert = messagebox.showerror('Error',result)
					return

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
						if story['story'] == trans['story'] and charm['charm'] == trans['charm']:
							text = text + 'TRANSPORT: {}'.format(trans['transport']) +'\n'
							for obj in self.master.objects:
								if obj['transport'] == trans['transport']:
									text = text+'Object Name: {}\nObject Type: {}\nDescription:\n{}\nAttachments:\n'.format(obj['objectName'],obj['objectType'],obj['description'])
									for file in self.master.files:
										if obj['objectId'] == file['objectId']:
											text = text+'{}\n'.format(file['dFileName'])
									text = text + '\n'
		return text
					
