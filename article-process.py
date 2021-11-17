# Writing this script as a test for the text comprehension algorithm
# Author: Noor Muhammad
# Date: Jan 27, 2021

# Holds the tokens to extract post entries from news websites.
# Since websites generate this content dynamically, parsing it
# with patters is easier.
import re

# Temporarily global vars, will be replaced later with a proper 
# mechanism
extracted_dates = []
extracted_proper_nouns = []

def remove_punctuation(token):
	"""Take a string and remove all punctuation from it"""

	# Regex to match non-alphanumeric
	regex_pattern = r'\W'
	replacer = re.compile(regex_pattern)
	return replacer.sub("", token)	

def extract_proper_nouns(line):
	"""Given a line of strings, extract proper nouns from it"""

	# Break the line into individual words, replacing - by space
	tokens = (" ".join(line.split("-"))).split(" ")
	
	# Remove punctuation, cleanup
	tokens = list(map(remove_punctuation, tokens))

	index = 0
	while index < len(tokens):
		# Capitalized token is a proper noun
		if tokens[index][0].isupper() == True:
		
			# logic to extract multi-token proper nouns
			compound_proper_noun = tokens[index]
		
			# While not on last element and the next token is also capitalized
			while index + 1 < len(tokens) and tokens[index+1][0].isupper() == True:
				# Add it to our compound proper noun
				compound_proper_noun += " " + tokens[index+1]
				# Skip this element in the outer loop
				index += 1

			# Only add if not available already
			if compound_proper_noun not in extracted_proper_nouns:
				extracted_proper_nouns.append(compound_proper_noun)
		index += 1

def extract_dates(line):
	"""Given a line of strings, extract dates from it"""
	pass

# Processes the lingual text of the website to extract key terms
def process_line(text_line):
	"""Process each line to tokenize and pull features."""
	
	# Dump trailing whitespace
	text_line = text_line.strip()

	# Extract proper nouns from the text and display them
	print("Now Processing line: {}...".format(text_line[0:50]))
	extract_proper_nouns(text_line)

	# Extract dates from the text and display them
	extract_dates(text_line)

	print("\n\n")

with open("news-sample", "r") as news_sample:
	for each_line in news_sample.readlines():
		# dump empty lines
		if each_line == '\n':
			continue
		else:
			process_line(each_line)

	print("Following proper nouns were extracted from the Article: ")
	print(extracted_proper_nouns)