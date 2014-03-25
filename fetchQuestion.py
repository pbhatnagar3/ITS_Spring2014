
#-----------------------------------------------------------------------
# fetchQuestion.py
#-----------------------------------------------------------------------
# Author: Pujun Bhatnaagar
# Semester: Spring 2014
# Team: Intelligent Review

import filt_concepts
import calculate_criticalness_score
import its_query as itsq
import its_table as itst

class fetchQuestion(object):
	filt_concepts_handle = None
	its_query_handle = None
	its_table_handle = None
	#Place to declare all the local variables
	
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
		
	# constructor	
	def __init__(self):
		
		self.its_query_handle = itsq.its_query()
		self.its_query_handle.open_connection()
		
		self.filt_concepts_handle = filt_concepts.filt_concepts()
		usedQuestions = []
		usedConcepts = []
		dictionary = self.filt_concepts_handle.concept_cross_correlation_dic
		#print dictionary
		#assuming that all the difficulty is being taken care
		for i in self.filt_concepts_handle.tier_one_condidate_concepts:
			#print i
			#all the concepts related to a particular concept
			temp = dictionary[i]
			#temp is a list of tuple
			#print temp
			#Query calculates tags, and total occurrences.
			for j in temp:				
				#query = "SELECT tags_id, COUNT(*) FROM questions_tags WHERE questions_id IN (SELECT id FROM questions WHERE " + self.get_category(0) +")  GROUP BY tags_id HAVING COUNT(*) >= 1"
				"""query = "select question from questions where id IN (select questions_id from questions_tags where tags_id =" + str(j[0]) + ")"
				print query
				resulting_questions = self.its_query_handle.exec_its_query(query)
				for k in resulting_questions:
					print k
				"""
				query_questions_ID_difficulty = "select q_id, difficulty from questions_difficulty where q_id IN (select questions_id from questions_tags where tags_id =" + str(j[0]) + ")"
				#print query_questions_ID_difficulty
				resulting_questions_difficulty = self.its_query_handle.exec_its_query(query_questions_ID_difficulty);
				resulting_questions_difficulty = sorted(resulting_questions_difficulty, key=lambda tup: tup[1], reverse = True)
				#print resulting_questions_difficulty[1][0]
				if len(resulting_questions_difficulty) > 1:
					result = (resulting_questions_difficulty[0][0], resulting_questions_difficulty[1][0])
				else:
					result = (resulting_questions_difficulty[0][0], 0)
				print result
				 
			
		
		
			

		
