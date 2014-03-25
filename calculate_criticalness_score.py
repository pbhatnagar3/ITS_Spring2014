#-----------------------------------------------------------------------
# calculate_criticalness_score.py
#-----------------------------------------------------------------------
# Author: Pujun Bhatnagar, Sen Lin
# Semester: Spring 2014
# Team: Intelligent Review
#-----------------------------------------------------------------------
# Mathematical Model: Criticalness = CC*(A*CS + B*IS)
#-----------------------------------------------------------------------
# Purpose: To calculate criticalness score (A*CS + B*IS) for each concepts 
#-----------------------------------------------------------------------
# Functions:
#	def __init__(self)
#	get_concepts_list(self)
# 	get_concepts_locations(self)
#	sort_concepts_class_level(self)
#   sort_concepts_individual_level(self)
#   generate_distribution(self, linear_distri)
#	get_class_linear_distribution(self)
#	get_individual_linear_distribution(self) 
#   calculate_criticalness(self)             
#-----------------------------------------------------------------------
# Define:
#	instance- instance of class user_stats class. This is 3D matrix.
#
#   concepts_list_class_level - Sorted a list of concepts by their difficulities
#                               in ascending order at class level   
#    
#   concepts_list_individual_level - Sorted a list of concepts by their difficulities
#                                     in ascending order at individual level
#
#	criticalness_Score_List -- A list contains calculated criticalness socre for all concepts
#
#	A -- weight index for class 
#
#	B -- weight index for individual
#-----------------------------------------------------------------------
# Note: Procedure for calculating (A*CS+ B*IS):
# 1. sort all concepts in by their difficulities
#    in ascending order at class level and individual level
# 2. generate linear distributions for the above two list, 
#    giving each concept a distribution score
# 3. get criticalness score through weighting their distribution score

import user_stats_updated
class calculate_criticalness_score(object):
#instance of class user_stats class
	instance = None
# Ranks
#  0           [(concept ID, difficulity), 
#  1            (concept ID, difficulity),
#  .            (concept ID, difficulity),
#  .            (concept ID, difficulity),
#  52           (concept ID, difficulity)]
	concepts_list_class_level = []
# Users/Ranks                 1                             2      ...         52
#  0           [(concept ID, difficulity), (concept ID, difficulity),... (concept ID, difficulity)]
#  1           [(concept ID, difficulity), (concept ID, difficulity),... (concept ID, difficulity)] 
#  .           [(concept ID, difficulity), (concept ID, difficulity),... (concept ID, difficulity)]
#  .           [(concept ID, difficulity), (concept ID, difficulity),... (concept ID, difficulity)]
#  230         [(concept ID, difficulity), (concept ID, difficulity),... (concept ID, difficulity)]
	concepts_list_individual_level = []
# Users/Ranks                 1                             2      ...                   52
#  0           [(concept ID, Criticalness Score), (concept ID, Criticalness Score),... (concept ID, Criticalness Score)]
#  1           [(concept ID, Criticalness Score), (concept ID, Criticalness Score),... (concept ID, Criticalness Score)] 
#  .           [(concept ID, Criticalness Score), (concept ID, Criticalness Score),... (concept ID, Criticalness Score)]
#  .           [(concept ID, Criticalness Score), (concept ID, Criticalness Score),... (concept ID, Criticalness Score)]
#  230         [(concept ID, Criticalness Score), (concept ID, Criticalness Score),... (concept ID, Criticalness Score)]
	criticalness_score_list = []
#	A -- weight index for class 
	A = 0.45
#	B -- weight index for individual
	B = 0.55
# constructor of the class
	def __init__(self,semester_id):
		self.instance = user_stats_updated.user_stats(semester_id)
		self.sort_concepts_class_level()	
		self.sort_concepts_individual_level()
		self.calculate_criticalness()
	#-------------------------------------------------------------------
	# Function: get_concepts_list(self)
	#-------------------------------------------------------------------
	# Purpose: To get a list that contains all concepts
	# Inputs: None
	# Output: A list contains all filted concepts
	#-------------------------------------------------------------------
	# Note: Called in get_concepts_locations.
	#-------------------------------------------------------------------
	def get_concepts_list(self):
		#A list concepts all concepts
		concepts_list = []
		for i in self.instance.concepts_2D:
			for j in i:
				if not j in concepts_list:
					concepts_list.append(j)
		return concepts_list
	#-------------------------------------------------------------------
	# Function: get_concepts_locations(self)
	#-------------------------------------------------------------------
	# Purpose: To find out how many times and where each concepts is used
	# Inputs: None
	# Output: A dictionary that contains each concepts 
	#         and their locations from concepts_2D matrix
	#-------------------------------------------------------------------
	# Note: Called in sort_concepts_class_level
	#-------------------------------------------------------------------
	def get_concepts_locations(self):
		
		structure = {}
		concepts_list = self.get_concepts_list()
		for j in concepts_list:
			list_number = 0;
			for i in self.instance.concepts_2D:
				list_number+=1;
				if j in i:
					temperary =[]
					temperary.append((list_number, i.index(j)))	
					if not j in structure:
						structure[j] = temperary
					else:
						temperary = temperary + structure[j]
						structure[j] = temperary
		return structure
	#-------------------------------------------------------------------
	# Function: sort_concepts_class_level(self)
	#-------------------------------------------------------------------
	# Purpose: To sort each concept by their difficulties in decesending order at class level
	# Inputs: None
	# Output: None
	#-------------------------------------------------------------------
	# Note: Called in the constructor
	#-------------------------------------------------------------------
	def sort_concepts_class_level(self):
		structure  = self.get_concepts_locations()
		final_list = []
		for i in structure:
			sum = 0;
			count = 0;
			for j in structure[i]:
				count+=1
				# temp is a 2D matrix that contains proficiency for all concepts vs all users 	
				temp = self.instance.user_concept_matrix_3D[j[0] - 1]
				for user in temp:
					# j[1] is a particular concept
					sum += user[j[1]]
				sum = sum/len(self.instance.users)
			sum = sum/count
			final_list.append((i, sum))
		self.concepts_list_class_level = sorted(final_list, key=lambda tup: tup[1])
	#-------------------------------------------------------------------
	# Function: sort_concepts_individual_level(self)
	#-------------------------------------------------------------------
	# Purpose: To sort each concept by their difficulties in decesending order at individual level
	# Inputs: None
	# Output: None
	#-------------------------------------------------------------------
	# Note: Called in the constructor
	#-------------------------------------------------------------------
	def sort_concepts_individual_level(self):
		structure  = self.get_concepts_locations()
		for user_count in range(0, len(self.instance.users)):
			structure2 = {}
			# summation of proficiency for each user for a particular concept from every assignment
			for j in range(1, self.instance.last_assignment ):
				temp_concepts = self.instance.concepts_2D[j-1]
				temp_values = self.instance.user_concept_matrix_3D[j-1][user_count]
				for k in temp_concepts:
					count = 0;
					if not k in structure2:
						structure2[k] = temp_values[count]
					else:
						structure2[k] = (structure2[k] + temp_values[count])
					count+=1
			final_list2 = []
			# get average of proficiency for a particular concept
			for i in structure2:
				structure2[i] = structure2[i]/len(structure[i])
				final_list2.append((i, structure2[i]))
			sorted_each_user = sorted(final_list2, key=lambda tup: tup[1])
			self.concepts_list_individual_level.append(sorted_each_user)
	#-------------------------------------------------------------------
	# Function: sort_concepts_individual_level(self)
	#-------------------------------------------------------------------
	# Purpose: To sort each concept by their difficulties in decesending order at individual level
	# Inputs: None
	# Output: A linear distribution for a list
	#-------------------------------------------------------------------
	# Note: Called in the constructor
	#-------------------------------------------------------------------		
	def generate_distribution(self, linear_distri):
		numOfConcepts = len(linear_distri)
		x = numOfConcepts /10
		distri_index = 1;
		counter = 0
		#Should by distri_index >= 0.5, but using this fathion can avoid floating error, 
		while distri_index > 0.48:
			for i in range(counter,counter+x):
				linear_distri[i] = (linear_distri[i][0],distri_index)
			counter += x
			distri_index -= 0.05
			if counter + x > numOfConcepts:
				x = numOfConcepts - counter
		return linear_distri	
	#-------------------------------------------------------------------
	# Function: get_class_linear_distribution(self)
	#-------------------------------------------------------------------
	# Purpose: At class level, generate linear distribution of each concept, 
	#          giving distribtion score to each concept
	# Inputs: None
	# Output: class_linear_distirbution
	#-------------------------------------------------------------------
	# Note: Called in calculate_criticalness
	#-------------------------------------------------------------------
	def get_class_linear_distribution(self):
		class_linear_distirbution = []
		class_linear_distirbution = self.generate_distribution(self.concepts_list_class_level)
		return class_linear_distirbution
	#-------------------------------------------------------------------
	# Function: get_individual_linear_distribution(self)
	#-------------------------------------------------------------------
	# Purpose: At individual level, generate linear distribution of each concept, 
	#          giving distribtion score to each concept
	# Inputs: None
	# Output: Individual_linear_distirbution
	#-------------------------------------------------------------------
	# Note: Called in calculate_criticalness
	#-------------------------------------------------------------------
	def get_individual_linear_distribution(self):
		individual_linear_distirbution = []
		for i in self.concepts_list_individual_level:
			individual_linear_distirbution.append(self.generate_distribution(i))
		return individual_linear_distirbution
	#-------------------------------------------------------------------
	# Function: calculate_criticalness(self)
	#-------------------------------------------------------------------
	# Purpose: This function calculates criticalness score for each concept 
	#           according to the mathematical model
	# Inputs: None
	# Output: None
	#-------------------------------------------------------------------
	# Note: Called in the constructor
	#-------------------------------------------------------------------
	def calculate_criticalness(self):
		temp_class = []
		temp_class = sorted(self.get_class_linear_distribution(), key=lambda tup: tup[0])
		temp_indi = []
		for i in range(0, len(self.get_individual_linear_distribution())):
			temp_indi.append(sorted(self.get_individual_linear_distribution()[i], key=lambda tup: tup[0]))
			for j in range(0, len(temp_class)):
				temp_indi[i][j] = (temp_class[j][0], self.A*temp_class[j][1] + self.B*temp_indi[i][j][1])
		self.criticalness_score_list = temp_indi

		
