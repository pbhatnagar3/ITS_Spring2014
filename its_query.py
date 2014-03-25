#-----------------------------------------------------------------------
# its_query.py
#-----------------------------------------------------------------------
# Author: Brian Nemsick (bnensick3)
# Semester: Spring 2014
# Team: Intelligent Review
#-----------------------------------------------------------------------
# Purpose: to handle all Python MySQL reading communication.
#-----------------------------------------------------------------------
# Functions:
#	close_connection(self)
# 	exec_its_query(self,my_query)
#	open_connection(self)
#-----------------------------------------------------------------------
# Notes:
# 	Can be used in any future projects.
#	Not used to write to databases.
#-----------------------------------------------------------------------
import MySQLdb as mdb
class its_query(object):
	#-------------------------------------------------------------------
	# Function: close_connection(self)
	#-------------------------------------------------------------------
	# Purpose: Close the ITS MySQL database handles.
	# Inputs: none
	# Outputs: none
	#-------------------------------------------------------------------
	def close_connection(self):
		self.cur.close()
		self.db.close()
	#-------------------------------------------------------------------
	# Function: exec_its_query(self,my_query)
	#-------------------------------------------------------------------
	# Purpose: Execute MySQL query.
	# Inputs: User MySQL query
	# Outputs: Result of MySQL query
	#-------------------------------------------------------------------
	def exec_its_query(self,my_query):
		self.cur.execute(my_query)
		return(self.cur.fetchall())
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
