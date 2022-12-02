from tkinter import messagebox

'''
	validation.py
'''

class Validate():
	''' validation for field input '''

	def __init__(self,master):
		self.master = master
		self.db_conn = self.master.db_conn
		self.objty = ['Function Module','Program','Table','Data Element','Domain','Structure']
		self.numbers = ['0','1','2','3','4','5','6','7','8','9']
		#self.objty = self.master.cr_obj_data.list_objty
		self.text = ''

	def validate_parent_data(self,parent,story,descr):
		''' change input validations'''
		if not parent or not story or not descr:
			self.text = 'Please fill out all fields!'
		elif len(parent) != 11 or parent[0:4] not in ['DFCT','ENHC']:
			self.text = 'Parent must be 11 characters and start with DFCT or ENHC!'
		elif len(story) != 11 or story[0:4] != 'STRY':
			self.text = 'Story must be 11 characters and start wit STRY'
		elif self.db_conn.select_table('parent','parent',parent).fetchone():
			self.text = 'An entry with key {} already exists'.format(parent)
		elif self.db_conn.select_table('parent','story',story).fetchone():
			self.text = 'An entry with key {} already exists'.format(story)
		return self.return_error()

	def validate_obj_data(self,transport,objectType,objectName,descr):
		''' object input validations'''
		if not transport or not objectType or not objectName or not descr:
			self.text = 'Please fill out all fields!'
		elif len(transport) != 10:
			self.text = 'Transport must be 10 characters long!'
		elif objectType not in self.objty:
			self.text = 'Please select an Object Type.'
		elif self.db_conn.select_table('transport','transport',transport).fetchone():
			self.text = 'An entry with key {} already exists'.format(transport)
		return self.return_error()

	def validate_charm_and_tran(self,charm,transport,descr):
		''' charm and transport validation '''
		if not charm or not transport or not descr:
			self.text = 'Please fill out all fields!'
		elif len(charm) != 10 or charm[0] != '9' or True in [x not in self.numbers for x in charm]:
			self.text = 'Charm must be 10 characters and start with 9'
		elif len(transport) != 10:
			self.text = 'Transport must be 10 characters long!'
		elif self.db_conn.select_table('transport','transport',transport).fetchone():
			self.text = 'An entry with key {} already exists'.format(transport)
		return self.return_error()

	def return_error(self): 
		''' returns an error if one triggered '''
		if self.text:
			alert = messagebox.showerror('Error',self.text)
			self.text = ''
			return False
		return True