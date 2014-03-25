#-----------------------------------------------------------------------
# its_table.py
#-----------------------------------------------------------------------
# Author: Brian Nemsick (bnensick3)
# Semester: Spring 2014
# Team: Intelligent Review
#-----------------------------------------------------------------------
# Purpose: to handle all Python MySQL writing communication.
#-----------------------------------------------------------------------
# Functions:
#	close_connection(self)
# 	construct_table(self,my_name,my_columns_f)
#	open_connection(self)
#	populate_table(self,my_name,my_columns,my_data)
#-----------------------------------------------------------------------
# Notes:
# 	Can be used in any future projects.
#-----------------------------------------------------------------------
import MySQLdb as mdb
class its_table(object):
	#-------------------------------------------------------------------
	# Function: close_connection(self)
	#-------------------------------------------------------------------
	# Purpose: Close the ITS MySQL database handles.
	# Inputs: none
	# Outputs: none
	#-------------------------------------------------------------------
	def close_connection(self):
		self.db.commit()
		self.cur.close()
		self.db.close()
	#-------------------------------------------------------------------
	# Function: construct_table(self,my_name,my_columns)
	#-------------------------------------------------------------------
	# Purpose: Construct a blank table with name, and column fields
	# Inputs: name, columns
	# Outputs: Empty table
	#-------------------------------------------------------------------
	def construct_table(self, my_name, my_columns_f):
		self.cur.execute("DROP TABLE IF EXISTS " + my_name)
		self.cur.execute("""CREATE TABLE """ + my_name + " " + my_columns_f)
	#-------------------------------------------------------------------
	# Function: open_connection(self)
	#-------------------------------------------------------------------
	# Purpose: Open the ITS MySQL database handles.
	# Inputs: none
	# Outputs: none
	#-------------------------------------------------------------------
	def open_connection(self):
		self.db = mdb.connect(host="localhost", user="root",
		passwd="csip", db="its")
		self.cur = self.db.cursor()
	#-------------------------------------------------------------------
	# Function: populate_table(self,my_name,my_columns,my_data)
	#-------------------------------------------------------------------
	# Purpose: Fills a MySQL table
	# Inputs: name, columns, data
	# Outputs: Populated table
	#-------------------------------------------------------------------	
	def populate_table(self, my_name, my_columns, my_data):
		self.cur.execute("""INSERT INTO """ + my_name + " " + my_columns + " " + """VALUES """ + my_data)
		
		
		
		
