import json 				# library for importing JSON
import random				# library for random numbers
from pprint import pprint	# library for printing dictionaries more readably
from modifiers import modifier_dictionary	# *local* library for Tracery modifiers
import os
# 
# Make your own Python port of Tracery, a text expansion library from Dr Kate
# An example Tracery tutorial http://air.decontextualize.com/tracery/
# A tracery editor by Dr Kate: artbot.club
# Bots and other resources on Tracery at BotWiki: 
#  https://botwiki.org/?s=tracery&search-filters-options%5B%5D=everything
#
# This assignment will use both recusion and dictionaries
# Unlike previous assignments, all the functions will be used as part of the 
# same algorithm.  So it is very important to test each individual function
# well, rather than trying to debug the whole algorithm

def load_grammar(path_to_grammar):
	""" 
	Load a JSON grammar file from a given path
	Parameters: 
		path_to_grammar(str): path to the grammar e.g. "grammars/cafe.json"
	Returns: 
		dict: a grammar that is a dictionary of strings or lists of strings (Tracery rules)
			e.g. {
					"animal": ["corgi", "wildcat", "otter", "antelope"],
					"color": ["magenta", "silver"],
					"origin": "Some #color# #animal.s# went to #place#"
				}
	"""

	with open(path_to_grammar) as json_file:
		return json.load(json_file)
	# Task 0: Load a grammar from JSON
	# Be sure to open the file with UTF-8 encoding, some grammars have non-english characters!
	# https://melaniewalsh.github.io/Intro-Cultural-Analytics/02-Python/07-Files-Character-Encoding.html

def get_key_count(grammar):
	""" 
	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
	Returns: 
		the total number of keys in this grammar
	"""

	# Task 1: Compute the number of keys in this grammar.  
	# You will want to use Python's built-in dictionary methods 
	# https://www.programiz.com/python-programming/methods/dictionary/keys
	# and "sum" https://www.programiz.com/python-programming/methods/built-in/sum
	return len(grammar.keys())
	

def get_rule_count(grammar):
	""" 
	e.g. {"a": ["apple", "anaconda"], "b": "banana"} => 3
	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
	Returns: 
		the total number of rules in this grammar
	"""
	# Task 2: Compute the number of rules in this grammar.  
	# You will want to use Python's built-in dictionary methods 
	# https://www.programiz.com/python-programming/methods/dictionary/values
	# Some values are *lists* and others are single strings. 
	# Maybe sure to count the number of rules, and not the number of characters
	# The function "isinstance(some_variable, list)"" will tell you if a variable is a list
	# (https://www.programiz.com/python-programming/methods/built-in/isinstance)

	count = 0
	for value in grammar.values():
		if isinstance(value, list):
			count += len(value)
		else:
			count += 1
	return count
	

def get_rule(grammar, key):
	"""
	Given a grammar and a key, find the rules for this key, select one randomly, and return it
		Parameters: 
			grammar(dict of lists or strings): a set of rule options for different keys
			key(str): a key that may be in the grammar
		Returns: 
			str: a randomly-selected rule from the grammar for this key if there is one
				if the key is *not* in this grammar, return "((key))" 
					for the name of that key, ie, "((animal))"
	"""

	# Task 3: given a key and a grammar (a dict), select a rule for that key
	# There are three cases to handle:
	# 	* that key is not in the grammar dict: return "((some_key))" for the name of the key
	# 	* the key is in the dict, and its value is a str, return the string (only one choice!)
	#	* the key is in the dict, and its value is a list, 
	#		use "random.choice" to return a randomly selected element of that list
	#		https://www.programiz.com/python-programming/modules/random

	if key in grammar:
		if isinstance(grammar[key], list):
			return random.choice(grammar[key])
		else:
			return grammar[key]
	else:
		return "((%s))" % key

def apply_modifiers(modifier_names, text):
	"""
	Given a dictionary of modifiers, a list of modifier names, and some text,
	return the result of applying each modifier by that name. 
	(Skip any modifiers where we don't have a modifier by that name)
	in order, to that text
	ie: "apple", ["a", "capitalize"] => "An apple"
	ie: "apple", ["s", "capitalizeAll"] => "APPLES"
	ie: "apple", ["capitalizeAll", "s"] => "APPLEs"
	
	Parameters:
		modifier_names(list is str): a list of modifier names "a", "s", "capitalize" to apply in order to the string
		text(str): the text to be changed
	Returns: 
		(str): the modified string 
	"""
	


	# Task 4: given a text (str), and a list of modifiers, and a dict of functions, 
	# 	return the result of modifing this string with each of those functions 
	#		(hint, use a for-loop to apply each modifier and replace 
	#		the current value of "text" with the modified version)
	#	Notice that we can store any kinds of Python variable in a dictionary: 
	#		lists, str, numbers, bools, even functions!
	#	When get a value from this dictionary, it will be a function, 
	# 		you can store that as a variable, just like you would with any other type
	# 		and then call it like any other function
	#		e.g.: 	"my_fxn = some_dict[some_key]" 
	#				"my_fxn(x, y, z)"
	# if the modifier is *not* in the dictionary, do nothing

	# NOTE: modifiers_dictionary(dict of functions) is a dictionary of 
	#   functions that take a string and return a modified copy of that string
	#	It is imported at the top of this file, and must be in the same directory as this file
	# print("The available modifiers are: ", modifier_dictionary.keys())
	for modifier in modifier_names:
		if modifier in modifier_dictionary:
			text = modifier_dictionary[modifier](text)
	return text
	
def expand_rule_section(grammar, section_text, index):
	"""
	*** A helper function for expand_text *** 
	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
		section_text(str): the text of this section "animal" or "animal.a.capitalize"
		index: the index of this section in the rule, this will determine if we need to expand it (odd) or not (even)
	Returns: 
		str: the expanded and modified rule (if we are expanding) or the section_text (if not)
	"""
	

	# Checking types!
	assert isinstance(grammar, dict), "expected a dict as grammar"
	assert isinstance(section_text, str), "expected a string as section_text"
	assert isinstance(index, int), "expected a int as index"

	# TASK 5: Expand this rule section
	# (This is a helper function for expand_rule, so we can test it independently -Dr. Kate)
	# For even sections (index%2==0), return the original section text (we don't need to do anything further)
	# For odd sections, this is a *socket* (ie, "animal.a.capitalize", and we need to figure out what to fill it with
	# To expand a socket:
	#  * split the socket text with "." to get a list (https://www.programiz.com/python-programming/methods/string/split)
	#  * the "key" for this socket is the *first* element in the list (ie: "animal")
	#  * the remaining elements are a list of modifier names (ie ["a", "capitalize"])
	#		* It may be an empty list! []
	#     (hint, you can use a "slice" to get a list containing all the remaining elements
	#     (https://www.programiz.com/python-programming/methods/built-in/slice))
	#  * get a rule for this key using "get_rule"
	#  * expand the rule using "expand_rule" (RECURSION!) to get the finished expanded rule
	#  * apply the modifiers to the expanded rule
	#  * return the final modified expanded rule

	if index%2 == 0:
		return section_text
	else:
		new_socket = section_text.split('.')
		key = new_socket[0]
		mod = new_socket[1:]
		key_rule = get_rule(grammar, key)
		expanded_rule = expand_rule(grammar, key_rule)
		mod_version = apply_modifiers(mod, expanded_rule)
		return mod_version

def expand_rule(grammar, rule):
	"""
	To expand a Tracery rule using a Tracery replacement grammar
	  e.g. "the #animal# went to #place# and ate #food#"
	* Split the text into a list of sections using text.split("#")
	* Create a *new list* from the list of sections using a list comprehension or a for loop
	*   For each section, use expand_rule_section to expand this section into its final form
	* Use "".join(some_list) to merge the list back into a single string
		https://www.programiz.com/python-programming/methods/string/join
		(note that just casting it to a string "str(some_list" would add unwanted commas)

	Hint: Using "enumerate" in your for-loop or list comprehension 
		will make it much easier to get an index to pass to "expand_rule_section"
	   https://realpython.com/python-enumerate/

	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
		rule(str): a Tracery rule to expand, e.g. "Some #color# #animal.s# went to #place.a#" 
			or "#color#" or "magenta"<-(no expansion needed for this one!)
	Returns
		str: the finished text of the expanded rule, e.g. "Some magenta corgis went to the zoo"
	"""

	# Task 6: Expand this rule (using the algorithm above, and the expand_rule_section helper function)
	
	sections = rule.split("#")
	expanded_sections = []
	for i, section in enumerate(sections):
		expanded_section = expand_rule_section(grammar, section, i)
		expanded_sections.append(expanded_section)
	expanded_rule = "".join(expanded_sections)
	return expanded_rule

def respond_to_input(grammar, user_input):
	"""
	Respond to some user input, like ELIZA did in 1969, by matching a pattern and generating a response
	e.g. https://web.njit.edu/~ronkowit/eliza.html

	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
		input(str): Something the user has said
	Returns
		str: the finished text of the response
	"""
	# Task 7: Return a response to the user's input.
	# Chatbots need to "listen" to the user, and generate a response.
	# This function makes a chatbot that can do three different things:
	# 	list all the grammar's keys if the user says "keys"
	#	respond with one of the expanded rules *if* the user's input includes one of the keys in this grammar
	#	respond to anything that doesn't match one of those two situations 
	# 		with an "unknown" rule (if we have that in the grammar)
	#		or with "I don't know how to respond to that" if we don't
	# Make sure that it can handle both upper and lower case situations 
	# 	(you may assume all grammar keys are lower case)

	# If the user says "keys", return all the keys in this grammar (ie, a list of things we know to talk about!)
	# If any of the keys of the grammar are found in the input, return the result of expanding "#some_key#"
	# If none do, but we have an "unknown" key, respond with the result of expanding "#unknown#"
	# Otherwise, return "I don't know how to respond to that"

	if user_input.lower() == "keys":
		return (grammar.keys())
	for key in grammar.keys():
		if key in user_input:
			return expand_rule(grammar, get_rule(grammar, key))
	if "unknown" in grammar:
		return expand_rule(grammar, '#unknown#')
	return "I don't know how to respond to that"


# Task 8
# Create your own grammar to create stories, or poetry, or dialogue, or fancy coffee drinks (whatever you want!)
# It should have at least 5 different keys, and at least 15 total rules, and an "origin" key that
# is the start of your generator.  
# **don't change the name from "my_grammar", it needs this same name for the autograder to read it!**

my_grammar = {
	"origin": ["#verb# #city# and #activity.lowercase# on the #direction# side of town. There you can meet #names#, who is #profession.a#."], 
	"verb": ['Visit', 'Travel to', 'Explore', 'Go to', 'Peruse', 'Visitar a'], 
	"city": ['Seattle', 'Chicago', 'Madrid', 'Copenhagen', 'Cape Town', 'London'],
	"activity": ['shop', 'eat', 'explore', 'swim', 'tour', 'watch shows', 'meet the locals'],
	'direction': ['north', 'south', 'east', 'west', 'northwest', 'northeast', 'southwest', 'southeast'],
	"names": ['Mr. Magoo', 'Dr. Doofus', 'Ms. Miss', 'Mrs. Name', 'Senor Schneef'],
	"profession": ['plumber', 'billionare', 'model', 'designer', 'engineer', 'dentist', 'construction worker']
}



if __name__ == '__main__':


	#----------------------------
	# Task 0

	# Load a known grammar to test against
	grammar_path = os.path.join("grammars", "simple.json")
	grammar = load_grammar(grammar_path)
	assert isinstance(grammar, dict), "The grammar should be a dictionary"
	assert "origin" in grammar, "There should be at least one key in this grammar, did you load it yet?"

	print(f"The keys of this grammar are {grammar.keys()}")
	
	# Pretty-print this grammar, format it nicely
	pprint(grammar) 

	# Task 1
	keyCount = get_key_count(grammar)
	print(f"There are {keyCount} keys in this grammar")
	assert keyCount == 5, "There should be 5 keys in the basic grammar, you had {keyCount}"
	
	# Task 2
	ruleCount = get_rule_count(grammar)
	print(f"There are {ruleCount} rules in this grammar")
	assert ruleCount == 19, "There should be 19 rules in the basic grammar, you had {ruleCount}"


	#----------------------------
	# Task 3

	# Random seeds allow us to generate the same random choices in a repeatable way
	# Calling random multiple times may cause you to get DIFFERENT ANSWERS than the asserts.
	# ** The main thing to watch for is that you get a *variety* of answers (it will repeat sometimes) 

	# Look, mostly different!
	for i in range(0, 7):
		print("get rule for 'animal': ", get_rule(grammar, "animal"))

	# Look, all the same!
	for i in range(0, 7):
		random.seed(10)
		print("get rule for 'animal', but with a seed: ", get_rule(grammar, "animal"))

	my_seed = 0

	# # We can set the seed, pick a random rule, and print it
	random.seed(my_seed)
	print(f"Getting a rule with seed {my_seed}:", get_rule(grammar, "animal"))
	# If we set the same seed, we will pick the same rule again!
	random.seed(my_seed)
	assert get_rule(grammar, "animal") == "corgi", "get_rule does not return 'corgi' for seed 0"

	my_seed = 10
	random.seed(my_seed)
	print(f"Getting a rule with seed {my_seed}:", get_rule(grammar, "animal"))
	random.seed(my_seed)
	assert get_rule(grammar, "animal") == "boa", "get_rule does not return 'corgi' for seed 0"
	assert get_rule(grammar, "insect") == "((insect))", f"{get_rule(grammar, 'insect')} is not the right format for missing keys, expecting: '((insect))'"
	assert get_rule(grammar, "origin") == "#adj.a# pack of #adj# #animal.s#", "Make sure you can handle if the rule is a single string, not a list"

	# #----------------------------
	# # Task 4

	# Test out the modifiers
	words = ["apple", "run", "flower", "mouse", "eagle"]
	for word in words:
		modified_word = apply_modifiers(["a", "capitalize"], word)
		print(f"{word} => {modified_word}")
	for word in words:
		modified_word = apply_modifiers(["ALLCAPS", "s"], word)
		print(f"{word} => {modified_word}")

	assert apply_modifiers(["a", "capitalize"], "coffee") == "A coffee" 
	assert apply_modifiers(["ALLCAPS", "s"], "coffee") == "COFFEEs" 
	
	# #----------------------------
	# # Task 5

	assert isinstance(expand_rule_section(grammar, "animal", 0), str), "expand_rule_section should return a string"

	random.seed(10)
	rule_section0 = expand_rule_section(grammar, "animal", 0)
	random.seed(10)
	rule_section1 = expand_rule_section(grammar, "animal", 1)
	random.seed(10)
	rule_section2 = expand_rule_section(grammar, "animal.a.capitalize", 1)
	print("EVEN:", rule_section0)
	print("ODD:", rule_section1)

	assert rule_section0 == "animal", "Even sections should return the text unaltered"
	assert rule_section1 == "boa", "Odd sections should expand the key for this socket"
	assert rule_section2 == "A boa", "Are you applying modifiers correctly?"

	# #----------------------------
	# # Task 6
	
	assert isinstance(expand_rule(grammar, "#animal#"), str), "Expand rule should return a string"

	plain_rule = "animal"
	medium_rule = "Hello, #animal#!"
	modifier_rule = "Hello, lots of #animal.s#"
	modifier_rule2 = "'#adj.a.ALLCAPS# AND #adj.ALLCAPS# #animal.ALLCAPS#!!', I exclaimed, in #adj.a# voice"
	complicated_rule = "#adj.a.capitalize# #animal#, and lots of #adj# #animal.s#"
	origin_rule = "#origin#"

	# Which rule to try out? Change this to test various rules
	current_rule = complicated_rule
	random.seed(0)
	print(f"Expanding '{current_rule}'")
	for i in range(0, 10):
		finished = expand_rule(grammar, current_rule)
		print(finished)
	

	random.seed(5)
	expansion1 = expand_rule(grammar, complicated_rule)
	print("expansion1:", expansion1)
	assert expansion1 == "A ((size)) corgi, and lots of eager boas", "It's ok if your output doesn't match this, but it should do the capitalization, plurals, and handling missing keys properly"
	
	random.seed(20)
	expansion2 = expand_rule(grammar, modifier_rule2)
	print("expansion2:", expansion2)
	assert expansion2 == "'AN ANCIENT AND EAGER BOA!!', I exclaimed, in an ambidextrous voice", "It's ok if your output doesn't match this, but it should do the capitalization, plurals, and handling missing keys properly"
	
	#----------------------------
	# Task 7
	# Try our your grammar, or the two sample grammars
	print("------------------------")
	random.seed(15)

	response0 = respond_to_input(grammar, "Tell me about an origin story")
	print(response0)
	response1 = respond_to_input(grammar, "What's your favorite animal?")
	print(response1)
	response2 = respond_to_input(grammar, "What's your favorite song?")
	print(response2)
	response2 = respond_to_input(grammar, "What's your favorite SONG???")
	print(response2)

	#This line changes the grammar
	grammar["unknown"] = "How about I tell your about #animal.s# instead?"
	response3 = respond_to_input(grammar, "What's your favorite song?")

	assert response0 == "an ancient pack of ambidextrous boas", "It's ok if your output is a different random expansion"
	assert response1 == "boa", "It's ok if your output is a different random expansion"
	assert response2 == "I don't know how to respond to that", ""
	assert response3 == "How about I tell your about emus instead?", "It's ok if your output is a different random expansion"
	
	#----------------------------
	# Task 8
	#Try out your grammar, or the two sample grammars
	grammar = load_grammar("grammars/cafe.json")
	grammar = load_grammar("grammars/magicschool.json")
	grammar = load_grammar("grammars/losttesla.json")
	grammar = my_grammar
	print(f"There are {get_key_count(grammar)} keys and {get_rule_count(grammar)} rules in this grammar")
	for i in range(0, 5):
		finished_rule = expand_rule(grammar, "#origin#")	
		print(finished_rule)

	#Test you bot by chatting with it live!
	#Note that input() will pause the program until you type something and press "enter"
	#and this while-loop won't terminate until we type "exit"

	user_input = ""
	print("------------------------")
	print("Testing your chatbot.  Type anything or 'exit' to stop")
	print(" (ask chef about dessert or coffee)")
	while user_input != "exit":
		user_input = input()
		print(respond_to_input(grammar, user_input))
