import sqlite3

'''
	db/sql.py
'''

class ConnectDB():
	''' establish connection with db and execute sql '''

	def __init__(self,path):
		# create a connnection with the db
		with sqlite3.connect(path) as self.c:
			self.cur = self.c.cursor()
			return

	def update_table(self,table,setField,setValue,whereField,whereValue):
		''' update table entries '''
		self.cur.execute('''UPDATE {} SET {} = "{}" WHERE {} = "{}"'''.format(
			table.strip(''),setField.strip(''),setValue.strip(''),whereField.strip(''),whereValue))
		self.c.commit()

	def insert_table(self,table,value):
		''' insert table entries '''
		v = ''
		if type(value[0]) == type(list()):
			# build the values insert based of number of supplied values
			for item in value[0]:
				v = v + '?,'
			try:
				self.cur.executemany('''INSERT INTO {0} VALUES({1})'''.format(table,v[:-1]),value)
			except(sqlite3.IntegrityError) as e:
				self.c.rollback()
				return 'Error when inserting. Entry already exists for {}'.format(e.args[0][26:])
		else:
			for item in value:
				v = v + '?,'
			try:
				self.cur.execute('''INSERT INTO {0} VALUES({1})'''.format(table,v[:-1]),value)
			except(sqlite3.IntegrityError) as e:
				self.c.rollback()
				return 'Error when inserting. Entry already exists for {}'.format(e.args[0][26:])

		self.c.commit()

	def delete_table(self,table=None,field=None,value=None):
		''' delete table entries '''
		if table == 'notes':
			value=value[0]
			self.cur.execute('''DELETE FROM notes WHERE noteid = {} AND notetxt = "{}" AND created = "{}"'''.format(value[0],value[1],value[2]))
		if table and not field and not value:
			self.cur.execute('''DELETE FROM {0}'''.format(table)) # delete entire table (development only)
		elif table and field and value:
			# delete specific entries
			self.cur.execute('''DELETE FROM {0} WHERE {1} = "{2}"'''.format(
														  															table,field.strip(''),value))
		else:
			print('please enter all parameters or only table')
			return
		self.c.commit()

	def select_table(self,table=None,field=None,value=None,max=False):
		''' select entries from db and return '''
		if table and field and value:
			return self.cur.execute('''SELECT * FROM {0} WHERE {1} = "{2}"'''.format(
																										table,field.strip(''),value.strip('')))
		if table and field and max:
			return self.cur.execute('''SELECT MAX({0}) FROM {1}'''.format(field.strip(''),table))

		if table:
			return self.cur.execute('''SELECT * FROM {}'''.format(table))


#--------------------------#
# QUICK TABLE MODIFICATION #
#--------------------------#

#with sqlite3.connect('db.db') as c:
	#cur = c.cursor()
	#cur.execute('''DROP TABLE parent''')
	#cur.execute('''DROP TABLE story ''')
	#cur.execute('''DROP TABLE change''')
	#cur.execute('''DROP TABLE transport''')
	#cur.execute('''DROP TABLE object''')
	#cur.execute('''DROP TABLE files''')
	#cur.execute('''DROP TABLE note_header''')
	#cur.execute('''DROP TABLE notes''')
	#c.commit()

	#cur.execute('''CREATE TABLE IF NOT EXISTS parent (parent TEXT UNIQUE NOT NULL,
	#																										descr TEXT NOT NULL,
	#																										status TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS story (parent TEXT NOT NULL,
	#																									story TEXT UNIQUE NOT NULL,
	#																									descr TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS charm (parent TEXT NOT NULL,
	#																									story TEXT NOT NULL,
	#																									charm TEXT UNIQUE NOT NULL,
	#																									descr TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS transport (transport TEXT UNIQUE NOT NULL,
	#																											charm TEXT NOT NULL,
	#																											descr TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS object (object_id INTEGER PRIMARY KEY AUTOINCREMENT,
	#																										transport TEXT NOT NULL,
	#																										object_type TEXT NOT NULL,
	#																										object_name TEXT NOT NULL,
	#																										descr TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS files (object_id INTEGER NOT NULL,
	#																									object_name TEXT NOT NULL,
	#																									transport TEXT NOT NULL,
	#																									file_name TEXT NOT NULL,
	#																									file_path TEXT UNIQUE NOT NULL,
	#																									file_id TEXT UNIQUE NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS note_header (noteid INTEGER PRIMARY KEY AUTOINCREMENT,
	#																									parent TEXT  NOT NULL,
	#																									descr TEXT NOT NULL,
	#																									status TEXT NOT NULL,
	#																									system TEXT NOT NULL)''')

	#cur.execute('''CREATE TABLE IF NOT EXISTS notes (noteid INTEGER NOT NULL,
	#																									notetxt TEXT NOT NULL,
	#																									created DATE NOT NULL)''')
	#c.commit()


#---------------------#
# ADHOC SQL EXECUTION #
#---------------------#

#obj = ConnectDB(path='db.db')
#obj.cur.execute('''DELETE FROM parent''')
#obj.cur.execute('''DELETE FROM story''')
#obj.cur.execute('''DELETE FROM charm''')
#obj.cur.execute('''DELETE FROM transport''')
#obj.cur.execute('''DELETE FROM object''')
#obj.cur.execute('''DELETE FROM files''')
#obj.cur.execute('''DELETE FROM note_header WHERE parent = "DFCT0019501"''')
#obj.cur.execute('''INSERT INTO note_header VALUES(NULL,'DFCT0019468','New storage locations for Denver FC','Created','Development')''')
#obj.cur.execute('''INSERT INTO note_header VALUES(NULL,'DFCT0019500','ADSI IDOC redistribution','Created','Development')''')
#obj.cur.execute('''INSERT INTO note_header VALUES(NULL,'DFCT0019501','Testing a bug','Created','Development')''')
#obj.cur.execute('''INSERT INTO parent VALUES('DFCT0019468','New storage locations for Denver FC','Created')''')
#obj.cur.execute('''INSERT INTO parent VALUES('DFCT0019500','ADSI IDOC redistribution','Created')''')
#obj.cur.execute('''INSERT INTO parent VALUES('DFCT0019501',' Testing a bug','Created')''')

#obj.c.commit()
