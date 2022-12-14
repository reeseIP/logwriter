from tkinter import messagebox

'''
	validation.py
'''

class Validate():
	''' validation for field input '''

	def __init__(self,master):
		self.master = master
		self.db_conn = self.master.db_conn
		self.systems = ['BD1','BW1','CR1','EC1','EW1','FI1','GRD','GT1','PI1','RD1','SC1','WD1']
		self.objty = ['Function Module','Program','Table','Data Element','Domain','Structure','Single Message']
		self.numbers = ['0','1','2','3','4','5','6','7','8','9']
		self.text = ''

	def validate_parent(self,parent):
		''' validate parent '''
		if len(parent) != 11 or parent[0:4] not in ['DFCT','ENHC']:
			text = 'Parent must be 11 characters and start with DFCT or ENHC!'
		else:
			text = None
		return text

	def validate_story(self,story):
		''' validate story '''
		if len(story) != 11 or story[0:4] != 'STRY':
			text = 'Story must be 11 characters and start wit STRY'
		else:
			text = None
		return text

	def validate_charm(self,charm):
		''' validate charm '''
		if len(charm) != 10 or charm[0] != '9' or True in [x not in self.numbers for x in charm]:
			text = 'Charm must be 10 characters, numeric, and start with 9'
		else:
			text = None
		return text

	def validate_transport(self,transport):
		''' validate transport '''
		if len(transport) != 10 and transport[0:3] not in self.systems:
			text = 'Transport must be 10 characters long and start with a valid system!'
		else:
			text = None
		return text

	def validate_object(self,object):
		''' validate transport '''
		if len(object) > 40:
			text = 'Object must be less than 40 chars'
		else:
			text = None
		return text

	def read_db(self,table,field,value):
		query = self.db_conn.select_table(table,field,value).fetchall()
		return query