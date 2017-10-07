# Implementation of the RAKE algorithm (Rapid Automatic Keyword Extraction)
# from Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley's 2010 Paper

# Prototype version, results match research paper but no additional functionality
# Score calculation function needs to be modified in order to work for longer documents -
#   current form is too slow and loops through text multiple times
# Need to implement ability to find adjoint keywords
# Uses nltk instead of regex for text seperation
# Time functions left in for testing purposes

# Author: aielk (https://github.com/aielk)

import time
import string
import nltk



# Loads a set of stop words from stop list file to use for creating candidate keyword phrases
# Using a set for stop words vastly decreases look up times when dealing with large bodies of text
#	in exchange for a small amount of upfront creation time. Differences noticeable after 50k words
# Punctuation is added to stop words to handle things like commas, periods, etc. after tokenization
def load_stop_list (filename):
	with open(filename) as inputfile:
		stop_words = set (inputfile.read().split())
		stop_words.update (set (string.punctuation))
		return stop_words

def load_text ():
	# Converting text to lowercase solves several issues and speeds up the program
	# Downside is that proper nouns will be lowercase in final results
	text = '''Compatibility of systems of linear constraints over the set of natural numbers.
	Criteria of compatibility of a system of linear Diophantine equations, strict inequations,
	and nonstrict inequations are considered. Upper bounds for components of a minimal set
	of solutions and algorithms of construction of minimal generating sets of solutions for all
	types of systems are given. These criteria and the corresponding algorithms for
	constructing a minimal supporting set of solutions can be used in solving all the
	considered types of systems and systems of mixed types.'''.lower().replace("\n", " ")
	return text

# Parses and splits the given text into words by utilizing nltk library  
def text_to_words (text):
	sentences = nltk.sent_tokenize (text)
	words = []
	for sentence in sentences:
		#if sentence[-1] in ".?,":
		#	sentence = sentence[:-1]
		words += nltk.word_tokenize (sentence)
#	words = [word for word in words if word not in string.punctuation]
	return words

# Goes through list of content words and creates candidate keyphrases by separating them at stop words
def create_candidate_keywords (text_words, stop_words):
	candidates = []
	keyword = []
	
	for word in text_words:
		if word in stop_words:
			keyword = " ".join (keyword)
			if keyword and keyword not in candidates:
				candidates.append (keyword)
			keyword = []
			continue
		keyword.append (word)
	
	keyword = " ".join (keyword)
	if keyword and keyword not in candidates:
		candidates.append (keyword)

	return candidates


def calculate_scores (text_words, candidate_keywords):
	result=[]
	for keyword in candidate_keywords:
		total=0
		for word in keyword.split():
			frequency = text_words.count (word)
			degree = sum([len(test.split()) for test in candidate_keywords if word in test.split()]) 
			#print (keyword, frequency, degree)
			total += degree / frequency
		
		result += [[total, keyword]]
	
	return result




sample_text = load_text()
stop_words = load_stop_list ("stoplist.txt")
words = text_to_words (sample_text)
keywords = create_candidate_keywords (words, stop_words)

start = time.time()


results = calculate_scores (words, keywords)

results.sort(reverse=True)
print(results[:15])


end = time.time()
print(end-start)

