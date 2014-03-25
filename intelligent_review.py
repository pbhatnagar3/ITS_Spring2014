#This quick test build will be eventually used for the demo and an individual user
#Easily expanded to more users by using a simple for loop
import concept_stats
import calculate_criticalness_score

class intelligent_review(object):
	
	#Define class handles
	concept_stats_handle = None
	calculate_criticalness_score_handle = None
	
	concept_lists = []
	
	
	def __init__(self,semester_id):
		
		#Open class handles
		self.concept_stats_handle = concept_stats.concept_stats()
		self.calculate_criticalness_score_handle = calculate_criticalness_score.calculate_criticalness_score(semester_id)
		
		#Calculate remaining meta data
		self.concept_order()
		
	def concept_order(self,chop_coeff = .05, min_coeff = .6, no_match_coeff = .5):
		score = []
		concepts = []
		#Calculate the critical correlation
		cc_concepts_sorted, cc_concepts_score = self.concept_stats_handle.critical_correlation(min_coeff,chop_coeff)
		#Loop over all possible concepts
		for concept1 in range(0,len(cc_concepts_sorted)):
			concepts.append(self.concept_stats_handle.cross_key[concept1])
			found = False
			for concept2 in range(0,len(self.calculate_criticalness_score_handle.criticalness_score_list[2])):
				#Checks for the match of the concepts 
				if (int(cc_concepts_sorted[concept1]) == int(self.calculate_criticalness_score_handle.criticalness_score_list[3][concept2][0])):
					found = True #Found concept
					score.append(cc_concepts_score[concept1] * float(self.calculate_criticalness_score_handle.criticalness_score_list[3][concept2][1])) #Found score
					break #Found what we needed in this iteration
			if (found == False):
				score.append(cc_concepts_score[concept1] * no_match_coeff) #Give a score if not found
		score,concepts = zip(*sorted(zip(score, concepts),reverse=True))
		self.concept_lists.append(concepts)
