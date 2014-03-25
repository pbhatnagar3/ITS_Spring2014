#-----------------------------------------------------------------------
# concept_stats.py
#-----------------------------------------------------------------------
# Author: Brian Nemsick (bnensick3)
# Semester: Spring 2014
# Team: Intelligent Review
#-----------------------------------------------------------------------
# Purpose: to calculate static concept statistics in ITS.
#-----------------------------------------------------------------------
# Functions:
#	__init__(self)
#	get_category(self,chapter)
# 	exec_its_query(self,my_query)
#	calc_meta_stats(self, filter_coeff)
#	calc_cross_correlation(self)
#	critical_correlation(self,lower_bound,chop)
#	create_tables(self)
#-----------------------------------------------------------------------
# Define:
#	key_concept_occurr - the number of assignments the concept is
#	contained in (minimum occurrence threshold).
#
#	concept_occurr - the number of assignments the concept is 
#	contained in (No thresholds).
#
#	total_questions - the number of questions associated with the 
#	concept.
#
#	cross_correlation (A,B) - given concept A, and concept B,
# 	given a question that concept A is tagged in the cross correlation
# 	defines the probability that concept B is also tagged.
#
#	total_correlation - the summation of cross_correlation of A for all
#	B.
#-----------------------------------------------------------------------
# Notes:
# 	Any calculations that have to do with user performance are not
#	handled within this class. The data output changes when concept
# 	tagging change or questions added/removed.
#
#	The principal goal of this class is to make con_per_assign.php, 
#	and corresponding table obsolete. Additional statistics have 
#	been added.
#-----------------------------------------------------------------------
import its_query as itsq
import its_table as itst

class concept_stats(object):
	its_query_handle = None
	its_table_handle = None
	#meta_stats (tag_id,total_questions,concept_occur,key_concept_occur)
	meta_stats = []
	#Used to map concept_ids to indexes for cross correlation
	#cross_key[0] = Concept0
	cross_key = []
	#Used to hold total correlation
	#total_correlation[0] = total_correlation[cross_key[0]]
	total_correlation = []
	# 		   Concept0, Concept1, Concept2,...
	# Concept0
	# Concept1
	# Concept2
	cross_correlation = []	
	def __init__(self):
		#Open Database
		self.its_query_handle = itsq.its_query()
		self.its_query_handle.open_connection()
		#Calculate Data
		self.calc_meta_stats()
		self.calc_cross_correlation()
		#Close Database
		self.its_query_handle.close_connection()
		#Create Tables
		self.create_tables()
	#-------------------------------------------------------------------
	# Function: get_category(self,chapter)
	#-------------------------------------------------------------------
	# Purpose: Find the associated assignment-categories of a given 
	# assignment.
	# Inputs: chapter - chapter #
	# Outputs: Associated assignment-categories that are used to 
	# construct an ITS assignment
	#-------------------------------------------------------------------
	# Note: A Python mirror of the output of /html/classes/its_query.php 
	# , getCategory function. A conversion of Greg's code.
	# HARDCODED
	#-------------------------------------------------------------------
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
	#-------------------------------------------------------------------
	# Function: calc_meta_stats(self, filter_coeff)
	#-------------------------------------------------------------------
	# Purpose: Calculate the defined concept meta stats.
	# Inputs: filter_coeff, minimum threshold
	#-------------------------------------------------------------------
	# Note: Called in the constructor.
	#-------------------------------------------------------------------
	def calc_meta_stats(self,filter_coeff = 3):
		#Query calculates tags, and total occurrences.
		query = "SELECT tags_id, COUNT(*) FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(0) +")  GROUP BY tags_id HAVING COUNT(*) >= 1"
		results = self.its_query_handle.exec_its_query(query)
		for tag_id in range (0,len(results)): 	
			self.meta_stats.append([int(results[tag_id][0]),int(results[tag_id][1]),0,0])
		#Query calculates, concept_occur, key_concept_occur
		for assignment_number in range(1, 8):
			query = "SELECT tags_id,COUNT(*) FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(assignment_number) +")  GROUP BY tags_id HAVING COUNT(*) >= 1"
			results = self.its_query_handle.exec_its_query(query)
			for tag_id in range (0,len(self.meta_stats)):
				for match_tag_id in range (0, len(results)):
					if (int(self.meta_stats[tag_id][0]) == int(results[match_tag_id][0])): #concept_occur
						self.meta_stats[tag_id][2] +=1
						if (int(results[match_tag_id][1]) >= int(filter_coeff)): #key_concept_occur
							self.meta_stats[tag_id][3]+=1
	#-------------------------------------------------------------------
	# Function: calc_cross_correlation(self)
	#-------------------------------------------------------------------
	# Purpose: Calculates the cross_correlation matrix
	# Inputs: None
	# Outputs: None
	#-------------------------------------------------------------------
	# Note: Called in the constructor.
	#-------------------------------------------------------------------
	def calc_cross_correlation(self):
		#Create the cross_key
		query = "SELECT tags_id FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(0) +")  GROUP BY tags_id HAVING COUNT(*) >= 1"
		tags = self.its_query_handle.exec_its_query(query)
		num_tags = len(tags)
		#Generate the cross_correlation
		for tag_index in range (0,len(tags)):
			self.cross_key.append(int(tags[tag_index][0]))
			query = "SELECT tags_id,COUNT(*) FROM questions_tags WHERE (questions_id IN (SELECT questions_id FROM questions_tags WHERE tags_id = " + str(self.cross_key[tag_index]) + " )) AND questions_id IN (SELECT id FROM questions WHERE " + self.get_category(0) +") GROUP BY tags_id HAVING COUNT(*) >= 1"
			results = self.its_query_handle.exec_its_query(query)
			cur_cross = [0] * num_tags
			for cross_tag_id in range (0,len(results)):
				for cross_id in range (0,len(self.cross_key)):
					if (int(results[cross_tag_id][0]) == int(self.cross_key[cross_id])):
						cur_cross[cross_id] = float(results[cross_tag_id][1])
			normalizer = max(cur_cross)
			for index in range (0,len(cur_cross)):
				cur_cross[index] = cur_cross[index]/normalizer
			self.cross_correlation.append(cur_cross)
			self.total_correlation.append(sum(cur_cross))
	#-------------------------------------------------------------------
	# Function: critical_correlation(self,lower_bound,chop)
	#-------------------------------------------------------------------
	# Purpose: Calculates the cross_correlation score for each concept.
	# Weighs them according to a linear alogirthm.
	# Inputs: lower_bound, chop
	# Outputs: concept_sorted, critical_score
	#-------------------------------------------------------------------
	# Note: Custom filter.
	#-------------------------------------------------------------------
	def critical_correlation(self,lower_bound,chop):
		critical_score = []
		total_correlation_sorted, concepts_sorted = zip(*sorted(zip(self.total_correlation, self.cross_key),reverse=True))
		curr_score = 1
		for rank in range(0,len(concepts_sorted)):
			curr_score = curr_score - (1-lower_bound)/len(concepts_sorted)
			if (rank <= chop*len(concepts_sorted)):
				critical_score.append(lower_bound)
			else:
				critical_score.append(curr_score)
		return (concepts_sorted,critical_score)
	#-------------------------------------------------------------------
	# Function: create_tables(self)
	#-------------------------------------------------------------------
	# Purpose: Dump cross_key and cross_correlation into MySQL Tables.
	# Inputs: None
	# Outputs: None
	#-------------------------------------------------------------------
	# Note: Called in constructor
	#-------------------------------------------------------------------
	def create_tables(self):
		#Open Handles
		self.its_table_handle = itst.its_table()
		self.its_table_handle.open_connection()
		#Calculate bulk data
		cross_key_data = ""
		cross_corr_data = ""
		cross_corr_columns = "(concept,"
		cross_corr_columns_f = "(concept CHAR(5),"
		for i in range(0, len(self.cross_key)):
			if (i > 0):
				cross_key_data = cross_key_data + ","
				cross_corr_data = cross_corr_data + ","
				cross_corr_columns_f = cross_corr_columns_f + ","
				cross_corr_columns = cross_corr_columns + ","
			cross_key_data = cross_key_data + "(" + str(i) + "," + str(self.cross_key[i]) + ")"
			cross_corr_data = cross_corr_data + "(c_" + str(i) + "," + ",".join(str(j) for j in self.cross_correlation[i]) + ")"
			cross_corr_columns_f = cross_corr_columns_f + " c_" + str(i) + " FLOAT" 
			cross_corr_columns = cross_corr_columns + " c_" + str(i)
		cross_corr_columns_f = cross_corr_columns_f + ")"
		cross_corr_columns = cross_corr_columns + ")"	
		#cross_key -> Table Construction
		self.its_table_handle.construct_table("""cross_key""","""(concept_index INT, concept INT)""")
		self.its_table_handle.populate_table("""cross_key""","""(concept_index,concept)""",cross_key_data)
		#cross_correlation -> Table Construction
		self.its_table_handle.construct_table("""cross_correlation""",cross_corr_columns_f)
		self.its_table_handle.populate_table("""cross_correlation""",cross_corr_columns,cross_corr_data)			
		#Close Handles
		self.its_table_handle.close_connection()
