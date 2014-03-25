########################################################################
# The following class is a python implementation of the existing user_stat.php
#file and is used to calculate the user statistics for all the students taking
#the class.
#Authors: Brian Nemsick and Pujun Bhatnagar
#Date: 8 February 2014
#
#
########################################################################
#importing its_query for communicating with the database
import its_query as itsq

#class implementation of user_stats (similar to user_stats.php)
class user_stats(object):
#making a debug handle
	debug = 0;
#delaring variables
	its_query_handle = None
#last assignment number
	last_assignment = 8
#the matrix that stores data for all the users
	user_concept_matrix = []
#the matrix that contains all the user information. Key to how things are arranged in user_concept_matrix
	users = []
#matrix containing all the concept and the numbers associated. Again, key to the user_concept_matrix
	concepts =[]
#booking keeping matrix that keeps a track of how many questions per concept
	total_questions_for_each_concept = []
#3-D data
	user_concept_matrix_3D = []
	concepts_2D = []
	total_questions_for_each_concept_2D = []
# constructor of the class
	def __init__(self,semester_id):
			#Open Database
			user_stats.its_query_handle = itsq.its_query()
			user_stats.its_query_handle.open_connection()
			#Calculate Data
			#calling the function that computes all the data for users and populates the matrix
			#self.calc_user_stats_all("Fall_2013", 7)
			#self.all_the_data("Fall_2013", 8)
			#self.calc_user_stats(1341, 1)
			#self.calc_user_stats(1342, 1)
			self.getUsers(semester_id)
			for i in range(1, self.last_assignment):
				self.getConcepts(i)
			if(self.debug == 1):
				"""print "The number of users: ",len(self.users)
				print "HERE IS A LIST OF ALL THE USERS", self.users
				print "here is a list of all the concepts for all the assignments"
				for i in range(0, self.last_assignment-1):
				print "for assignment ", i+1, self.concepts_2D[i], "\n";
				self.calculate_all_user_stats_single_assignment(1)
				print self.user_concept_matrix
				print len(self.user_concept_matrix)
				"""
			self.calculate_all_user_stats_all_assignments(self.last_assignment)	
			#Close Database
			user_stats.its_query_handle.close_connection()

#this method gets all the users for a given semester and saves it into the users list
	def getUsers(self, semester):
		#figure out all the users
		query = "SELECT id from users where status = \"" + str(semester) +"\" ;"
		#one can uncomment it for debugging purposes
		#print query
		result = user_stats.its_query_handle.exec_its_query(query)
		for i in result:
			self.users.append(i[0])

#this function gets all the important concepts for each assignment
	def getConcepts(self,ass_num,s_id = 1341, filter_coeff = 3):
		#making the 1 dimentional lists to be null or empty again
		self.concepts = []
		self.total_questions_for_each_concept = []
		ind_user = [] #C_ID, Question, Percent
		#Find concepts, number of questions
		query = "(SELECT tags_id,COUNT(*) FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(ass_num) +") GROUP BY tags_id HAVING COUNT(*) >= " + str(filter_coeff) +")"
		concepts = user_stats.its_query_handle.exec_its_query(query)	
		#Find user proficiency
		for concept in range (0,len(concepts)):
			query = "SELECT avg(score) FROM stats_" + str(s_id) + " WHERE current_chapter = " + str(ass_num) + " AND question_id IN (SELECT questions_id FROM questions_tags WHERE tags_id = "+ str(concepts[concept][0]) + ")"
			results = user_stats.its_query_handle.exec_its_query(query)	
			if (str(results[0]) == '(None,)'):
				ind_user.append([int(concepts[concept][0]),int(concepts[concept][1]),0])
			else:
				ind_user.append([int(concepts[concept][0]),int(concepts[concept][1]),float(results[0][0])])	
		temp = []
		for concept, question, percent in ind_user:
			self.concepts.append(concept)
			self.total_questions_for_each_concept.append(question)
		#print "here are the concepts for assignment " , ass_num, self.concepts
		self.concepts_2D.append(self.concepts)
		self.total_questions_for_each_concept_2D.append(self.total_questions_for_each_concept)

#this function computes the user_stat information for a single user for a single assignment
	def calculate_user_stats(self,s_id,ass_num,filter_coeff = 3):
		ind_user = [] #C_ID, Question, Percent
		#Find concepts, number of questions
		query = "(SELECT tags_id,COUNT(*) FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(ass_num) +") GROUP BY tags_id HAVING COUNT(*) >= " + str(filter_coeff) +")"
		concepts = user_stats.its_query_handle.exec_its_query(query)

		#Find user proficiency
		for concept in range (0,len(concepts)):
			query = "SELECT avg(score) FROM stats_" + str(s_id) + " WHERE current_chapter = " + str(ass_num) + " AND question_id IN (SELECT questions_id FROM questions_tags WHERE tags_id = "+ str(concepts[concept][0]) + ")"
			results = user_stats.its_query_handle.exec_its_query(query)

			if (str(results[0]) == '(None,)'):
				ind_user.append([int(concepts[concept][0]),int(concepts[concept][1]),0])
			else:
				ind_user.append([int(concepts[concept][0]),int(concepts[concept][1]),float(results[0][0])])

		temp = []
		#appending data to the concept_matrix
		for concept, question, percent in ind_user:
			temp.append(percent/100)
		self.user_concept_matrix.append(temp)

#this function computes user_stat info for all users for a single assignment
	def calculate_all_user_stats_single_assignment(self, assignment):
		for user in self.users:
			self.calculate_user_stats(user, assignment)

#this function computes user_stats for all users for all assignments
	def calculate_all_user_stats_all_assignments(self, last_assignment_number):
		for current_assignment in range(1, last_assignment_number):
			self.user_concept_matrix = []
			self.calculate_all_user_stats_single_assignment(current_assignment)
			self.user_concept_matrix_3D.append(self.user_concept_matrix)

#The following function ...
	def get_category(self,chapter):
		return {
		0: """category REGEXP "(SPEN1$|PreLab01$|Lab1$|Chapter1$|-Mod1$|Complex$|SPEN2$|PreLab02$|Lab2$|Chapter2$|-Mod2$|SPEN3$|PreLab03$|Lab3$|Chapter3$|-Mod3$|SPEN4$|PreLab04$|Lab4$|Chapter4$|-Mod4$|SPEN5$|PreLab05$|Lab5$|Chapter5$|-Mod5$|SPEN6$|PreLab06$|Lab6$|Chapter6$|-Mod6$|SPEN7$|PreLab07$|Lab7$|Chapter7$|-Mod7$)" AND questions.qtype IN ("MC","M","C")""",
		1: """category REGEXP "(SPEN1$|PreLab01$|Lab1$|Chapter1$|-Mod1$|Complex$)" AND questions.qtype IN ("MC","M","C")""",
		2: """category REGEXP "(SPEN2$|PreLab02$|Lab2$|Chapter2$|-Mod2$)" AND questions.qtype IN ("MC","M","C")""",
		3: """category REGEXP "(SPEN3$|PreLab03$|Lab3$|Chapter3$|-Mod3$)" AND questions.qtype IN ("MC","M","C")""",
		4: """category REGEXP "(SPEN4$|PreLab04$|Lab4$|Chapter4$|-Mod4$)" AND questions.qtype IN ("MC","M","C")""",
		5: """category REGEXP "(SPEN5$|PreLab05$|Lab5$|Chapter5$|-Mod5$)" AND questions.qtype IN ("MC","M","C")""",
		6: """category REGEXP "(SPEN6$|PreLab06$|Lab6$|Chapter6$|-Mod6$)" AND questions.qtype IN ("MC","M","C")""",
		7: """category REGEXP "(SPEN7$|PreLab07$|Lab7$|Chapter7$|-Mod7$)" AND questions.qtype IN ("MC","M","C")""",
		8: """category REGEXP "(SPEN1$|PreLab01$|Lab1$|Chapter1$|-Mod1$|Complex$|SPEN2$|PreLab02$|Lab2$|Chapter2$|-Mod2$|SPEN3$|PreLab03$|Lab3$|Chapter3$|-Mod3$|SPEN4$|PreLab04$|Lab4$|Chapter4$|-Mod4$|SPEN5$|PreLab05$|Lab5$|Chapter5$|-Mod5$|SPEN6$|PreLab06$|Lab6$|Chapter6$|-Mod6$)" AND questions.qtype IN ("MC","M","C")""",
		}[chapter]
