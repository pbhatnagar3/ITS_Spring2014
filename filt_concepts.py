
#-----------------------------------------------------------------------
# filt_concepts.py
#-----------------------------------------------------------------------
# Author: Sen Lin
# Semester: Spring 2014
# Team: Intelligent Review
import concept_stats
class filt_concepts(object):
	concept_stats_handle = None
	# a dictionar which use each concept ID as key,
	# and its most relevant concepts and their cross correlation score as value
	concept_cross_correlation_dic = {}
	# This list doesn't concern about criticalness of each concept. 
	# It only concerns about occurance and how it's relevant to other concepts
	tier_one_condidate_concepts = []
	# This list doesn't concern about criticalness of each concept. 
	# It only concerns about occurance and how it's relevant to other concepts
	tier_two_condidate_concepts = []
	# construtor of the class
	def __init__(self): 
		self.concept_stats_handle = concept_stats.concept_stats()
		self.concept_cross_correlation_dic  = self.get_concept_cross_correlation_dic(1)
		# We have 16 condidates for tier one
		self.tier_one_condidate_concepts  = self.get_candidate_concepts_by_tier(1)
		# We have 40 condidates for tier two
		self.tier_two_condidate_concepts  = self.get_candidate_concepts_by_tier(2)
	#-------------------------------------------------------------------
	# Function: get_concept_cross_correlation_dic(self)
	#-------------------------------------------------------------------
	# Purpose: create a dictionary which use each concept ID as key,
	#           and its most relevant concepts and their cross correlation score as value
	# for example 120: [(40, 0.1875), (118, 0.125), (127, 0.125), (70, 0.0625)]. 
	# 					concept # 40 is most relevant to concept # 130, and so on. 
	# Inputs: None
	# Output: None
	#-------------------------------------------------------------------
	# Note: Called in calculate_criticalness
	#-------------------------------------------------------------------
	def get_concept_cross_correlation_dic(self, filter):
		dic = {}
		cross_correlation = self.concept_stats_handle.cross_correlation
		cross_key = self.concept_stats_handle.cross_key
		for concept_index in range (0, len(cross_key)):
			tempList = []
			for index in range (0,len(cross_correlation[concept_index])):
				if (cross_correlation[concept_index][index] > 0 and cross_correlation[concept_index][index] != 1):
					tempList.append((cross_key[index],float(cross_correlation[concept_index][index])))
			tempList = sorted(tempList, key=lambda tup: tup[1], reverse = True)
			concept = cross_key[concept_index]
			if (len(tempList) >= filter):
				dic[concept] = tempList
		return dic
	def get_candidate_concepts_by_tier(self, tierNum):
		if (tierNum == 1):
			# This would generate a list contains 20 concepts
			keyConceptFilter = 2
			# This would generate a dictionary contains 58 concepts
			cross_correlation_filter = 2
		if (tierNum == 2):
			# This would generate a list contains 53 concepts
			keyConceptFilter = 1
			# This would generate a list contains 69 concepts
			cross_correlation_filter = 1
		# this list contains most occurant concepts
		list1 = []
		dic = self.get_concept_cross_correlation_dic(cross_correlation_filter)
		meta_stats = self.concept_stats_handle.meta_stats
		for index in range (0, len(meta_stats)):
			if (meta_stats[index][3] >= keyConceptFilter):
				list1.append((meta_stats[index][0],meta_stats[index][3]))
		list1 = sorted(list1, key=lambda tup: tup[1], reverse = True)
		# This list contains concepts having intersections between 
		# a list having most occurance concepts and a dictionary which its keys have most number of relavent concepts
		list2 = []
		for index in range (0, len(list1)):
			for key in dic.keys():
				
				if (list1[index][0] == key):
					list2.append(key)
		return list2
			
	
			
		
		
