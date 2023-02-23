"""
In this assignment, we will build a class "WikiPage" that stores 
information about individual wikipedia pages 

e.g. Raising_of_Chicago

and use that class to build 
* a directory of pages (a dict of WikiPage instances) 
* indexed by the page name (eg. "raising_of_chicago")

to make queries and display charts of how pages are connected

**** BEFORE YOU START *****

We are using a couple of external libraries:

* BeautifulSoup, which parses HTML in a convenient way
* Treelib, which easily visualize tree-shaped data 
(https://www.freecodecamp.org/news/all-you-need-to-know-about-tree-data-structures-bceacb85490c/)

If working in the command line or a local IDE, 
you will need to install libraries using PIP (a python package manager)
If you have a mac, you probably already have it installed, otherwise
follow these instructions:

https://www.makeuseof.com/tag/install-pip-for-python/
You can then type pip (or pip3 depending on your installation)
* pip3 install beautifulsoup4
* pip3 install treelib

You can also open up a wikipedia page's source to see 
how an HTML page (particularly a wiki article) is structured

Paste this in your browser: 
view-source:Cat

HTML elements can have 
* an id (a unique identifier)
* a type (each element only has one type, like "div", or "img")
* a class (many elements can all have the same class, 
	and an element can have many classes, like "neon_style" or "optional_user", etc)

In this assignment, we will use Beautiful Soup to explore 
the elements in an HTML site
https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/

"""

from load_url_politely import load_url_politely
from bs4 import BeautifulSoup
import re
from treelib import Node, Tree
from datetime import datetime
from collections import Counter
from pprint import pprint
import random



def get_title(soup):
	assert isinstance(soup, BeautifulSoup), "Expected a soup object"
	
	"""
	How do you find an element, like a title tag
	"<title>My Cool Page</title>" in Beautiful Soup?
	
	Given some BeautifulSoup instance ("soup"), 
	get the title of this page 
	
	Getting data from a soup object:
	We can get an element from a soup instance in many different ways
	(see get_all_links for more)

	One way is to get the *first* element of some type, 
	which we can do through the "." notation, like
	soup.h3 or soup.a or soup.title, to get the html's first
	<h3> or <a> or <title> tag

		Parameters: soup (bs4.BeautifulSoup): a processed HTML page
		Returns: str: the string of its page title 
			(up to the first dash, we don't need "Cat - Wikipedia", 
			we just want "Cat")

	(remember that you can use some_text.find("some_substring")
	to find the index of a substring in some text, 
	and can use that index to make a *slice* of the text
	e.g: text[0:text.find(some_substring_to_remove_from_the_end)])
	"""

	# Uncomment to explore ways to access elements in a soup object:
	# What type is "soup"?
	print(type(soup))
	#Example (uncomment to see)
	
	#print("The first h3 element is", soup.title)
	#print(f"The first h3 element's text is '{soup.h3.text}'")

	# Task 0: Get the title of the page, and return it (minus " - Wikipedia")

	title = soup.title.text
	final = title[0:title.find(' - Wikipedia')]
	return final


def get_last_edit(soup):
	assert isinstance(soup, BeautifulSoup), "Expected a soup object"
	
	"""
	How do you find elements with an id in Beautiful Soup?

	The last edit on a wiki page has an id:
		id="footer-info-lastmod"

	Previously we got the first element with a *type*
	Now we have to get an element by an id 
	* You can do that with soup.find(id="some_id_name")
	* We also want the *text*, not the whole element, 
		so use the .text to get the text contents
	* Finally, we don't want the whole text, 
		just a substring of everything after the prefix
		and not including the last period
	
	All last-edits in Wikipedia are of the format 
	" This page was last edited on 9 November 2021, at 13:44"

		Parameters: soup (bs4.BeautifulSoup): a processed HTML page
		
		Return all the text between the substring " on " and ", at"
		e.g: "9 November 2021"
	
	"""

	# The substrings that surround the information we want
	start_text = " on "
	end_text = ", at"

	# Example:
	print(f"the copyright element is: {soup.find(id='footer-info-copyright')}")
	print(f"the copyright element's text is: {soup.find(id='footer-info-copyright').text}")

	# Task 1: Get date of the last edit of this page (e.g. 9 November 2021)
	date = soup.find(id='footer-info-lastmod').text
	final = date[date.find(start_text) + 4:date.find(end_text)]
	return final
	


def get_wordcount(soup):
	assert isinstance(soup, BeautifulSoup), "Expected a soup object"
	"""
	Beautiful Soup objects contain a tree of elements 
	We can look at either individual elements 
	(all the <div> and <p> and <img> elements, etc), 
	or just the inner text of the elements (ignoring all the HTML markup)
	using some_element.text (Note: its a *property* and not a method) 
	**To get just the text of a whole page, use "soup.text"**

	To get individual words from text, you can use Python's "split" method
	If used without any parameters, it will split on any "whitespace"
	(spaces, tabs, newlines, etc)
	https://www.programiz.com/python-programming/methods/string/split

	Use these two techniques to return the number of words in this article

		Parameters: soup: a BeautifulSoup instance (some parsed HTML)
		Returns: (int) the number of words in this article
	"""

	# Example:
	# print("The raw HTML of this page: ", str(soup)[0:100])
	# print("The *text* of this page: ", soup.text[0:100])
	# print("""some text 	to 		
	# 	split up""".split())


	# Task 2: Get wordcount of this page

	words = soup.text
	wc = words.split()
	return len(wc)





def get_all_links(soup):
	assert isinstance(soup, BeautifulSoup), "Expected a soup object"
	
	"""
	How do you find *all* the tags of a type in Beautiful Soup?

	We can use soup.find_all() to find all elements of some type or class
	Consider the example below, and use it as a template for code to
	* get all the "a" tags in the soup (links), 
	* and return a list of all the "href" attributes (the link urls)

		Parameters: soup: a BeautifulSoup instance (some parsed HTML)
		Returns: (list of strings) all URLs linked to in this page
	"""
	

	# Example: find all the image alt-text in this page
	# * find all the img tags in this soup
	# * for each img tag, see if it has an "alt" attribute 
	#    (captioning for photos)
	# * if it has that attribute, add that alt attribute to the list 

	# all_images = soup.find_all("img")
	# all_alt_text = []
	# for img in all_images:
	# 	if "alt" in img.attrs and img.attrs["alt"] != "":
	# 		all_alt_text.append(img.attrs["alt"])
	# print(f"found {len(all_alt_text)} alt-texts:", all_alt_text)

	# Task 3: Using the example above, get all the "href" 
	#   (the url of a link) values for all "a" tags to 
	#   get a list of all urls linked to in this page

	all_a = soup.find_all('a')
	all_tag = []
	for tag in all_a:
		if "href" in tag.attrs and tag.attrs['href'] != '':
			all_tag.append(tag.attrs['href'])
	return all_tag

def get_all_wiki_link_ids(soup):
	"""
	We can get a list of all links, using "get_all_links" above
	Can we use that to get a list of all wiki article ids 
	(e.g. Thank_U,_Next_(song), Cat, Evanston,_Illinois)
	that are linked to?

	Each link to another article in wikipedia has the format
	"/wiki/Article_ID", e.g "/wiki/Cat", "/wiki/Thank_U,_Next_(song)"
	If we take a slice starting at 6 or links like these, we can get *just the id*
	
	Some links have ":" or "#" in them: "/wiki/Category:Cats", "/wiki/Red_panda#Taxonomy"
	but these are for resources, subsections or category articles and we don't want those

	Use a for-loop or a list comprehension to return a list 
	of *just* the wiki article ids from URLS that:
	* start with "/wiki/"
	* don't have ":" or "#"
	BE sure to get the part of the link *without* "/wiki/" 

		Parameters: soup: a BeautifulSoup instance (some parsed HTML)
		Returns: (list of strings) all wiki article ids linked to in this page
			e.g. 'Single_(music)', 'Ariana_Grande', 'A-side_and_B-side', 'Imagine_(Ariana_Grande_song)'
			(links from the "Thank You, Next" article)

	"""

	# Task 4: get all of the wiki article ids linked from this page
	links  = get_all_links(soup)
	link_arr =[]
	for id in links:
		if id.startswith('/wiki/') and ':' not in id and '#' not in id:
			link_arr.append(id[6:])
	return link_arr

def get_shortest_page(page_directory):
	"""
	Recall how in A1 you had to find the most northern student?
	Use the same approach here to find the *shortest* article (ie the least wordcount)

	Parameters: 
		page_directory (dict): a dictionary of WikiPage instances that we have loaded
	Returns: 
		the WikiPage with the least wordcount
	"""
	
	# Task 6: Find the shortest article

	# Assuming no wiki articles have more than a million words, any article will beat this
	winning_count = 999999 
	winner = None
	for page in page_directory.values():
		count = page.wordcount
		if count < winning_count:
			winner = page
			winning_count = count
	return winner

def get_oldest_page(page_directory):
	"""
	https://stackoverflow.com/questions/466345/converting-string-into-datetime
	The same as get_shortest_page, but how do we compare dates?
	We can use a not-very-readable python trick to turn it into a timestamp
	"timestamp = datetime.strptime(page.last_edit, '%d %B %Y')"
	which we can then compare like a normal number: e.g. "time_a < time_b"

	Parameters: 
		page_directory (dict): a dictionary of WikiPage instances that we have loaded
	Returns: 
		the WikiPage with the oldest last-edit property
	"""
	
	# Task 7: Find the oldest article

	# The timestamp for right now, any article is older than this
	winning_timestamp = datetime.today() 
	winner = None
	for page in page_directory.values():
		timestamp = datetime.strptime(page.last_edit, '%d %B %Y')
		if timestamp < winning_timestamp:
			winner = page
			winning_timestamp = timestamp
	return winner


class WikiPage:
	def __init__(self, page_directory, page_id):
		"""
		Load this page (from Wikipedia or our cache)
		Creates a BeautfulSoup object from the loaded HTML 
		Store this instance in a page_directory under the key of its page_id 
			(ie "Thank_U,_Next_(song)")
		Sets the url, html, soup, wordcount, last_edit, page_id
			and wiki_links of this instance

		Parameters:
			page_directory: a dictionary of all the pages we have loaded so far, 
				organized by their page_id
			page_id(str): the wikipedia page id, like "Thank_U,_Next_(song)"
			
		"""
		
		# Some asserts to catch if we pass in the wrong parameters
		assert isinstance(page_directory, dict), f"page_directory should be a dict not {page_directory}"
		assert not page_id.startswith("/wiki/"), "Expecting just the id a wiki article, not /wiki/some_id"
		assert not page_id.startswith("http"), "Expecting just the id of a wiki article, not the full url"

		# This is a useful line to alert you whenever you create a new WikiPage
		# Helps catch bugs if you are creating WikiPages multiple times, unintentionally
		# print(f"\n★ Create WikiPage for '{page_id}'")

		# Create the URL of this page 
		# (what we need to pass to the load_url_politely function)
		wiki_prefix = "https://en.wikipedia.org/wiki/"
		self.url = wiki_prefix + page_id
		
		# Task 5 
		# We need to do a lot of things to initialize a wiki page
		#   but we already have functions for most of them 
		# 	(...and there are examples of the others in __main__)
		# * Add this WikiPage instance to the page_directory using its page_id as the key
		# * Use load_url_politely to load HTML from page's URL (from cache or Wikipedia)
		# 	**READ THE LOAD URL POLITELY FILE TO SEE HOW TO USE IT!***
		# * Create a BeautifulSoup instance for this HTML
		# * Store the title, wordcount, page_directory, page_id, 
		#  		and last_edit as properties on this instance
		# * Calculate all the wiki link ids using get_all_wiki_link_ids 
		#		and store it as a wiki_links property on this instance
		
		self.html = load_url_politely(self.url)
		self.soup = BeautifulSoup(self.html)
		self.title = get_title(self.soup)
		self.wordcount = get_wordcount(self.soup)
		self.page_directory = page_directory
		self.page_id = page_id
		self.last_edit = get_last_edit(self.soup)
		self.wiki_links = get_all_wiki_link_ids(self.soup)
		page_directory[page_id] = self



	def get_interesting_links(self):
		# The newest version of Wikipedia puts boring links (to Main Page, etc) at the top.
		# We can make our data science more interesting by making a copy of wiki_ids
		# with the boring ones *FILTERED OUT*

		# Look, a list comprehension! 
		all_interesting = [wiki_id for wiki_id in self.wiki_links if "Main_Page" not in wiki_id and "_(album)" not in wiki_id]

		# Remove duplicates
		# https://stackoverflow.com/questions/480214/how-do-i-remove-duplicates-from-a-list-while-preserving-order
		return list(dict.fromkeys(all_interesting)) 
		

	def load_links(self, recursion_count=0, links_per_article=5, randomize_links=False):
		"""
		Load the pages linked to from this article by making new
		WikiPage instances for them

		Note that many pages have hundreds of Wiki articles linked,
		so we only want to load the first "links_per_article"
		"""


		# **Trick for printing out recursive function information:**
		# Indent the output with the amount of recursion
		spacer = "\t"*(5 - recursion_count)
		print(spacer + f"➡ LOADING LINKS {links_per_article} links from {self.title}, recursion count {recursion_count} (this number should go down)")
		
	

		# Task 8: load all links from this
		# Get all the "interesting links" from this page (see above)
		# 	If randomize_links is true, use "shuffle" to randomly re-order them
		# 	https://www.w3schools.com/python/ref_random_shuffle.asp
		#	Pick the first N links (using links_per_article)
		# 		to make a *shorter* list of links to load

		# 	(ie, ['Felidae', 'Cat_(disambiguation)', 'Cats_(disambiguation)', 
		#   'Conservation_status', 'Taxonomy_(biology)'] in the Cats article)
		

		# For each wiki id, 
		# 	* if it is not already in the directory
		#		* Create a WikiPage instance for this page_id
		#			* it needs a page_directory too, let's give it ours
		#		* RECURSIVELY expand the links of this new page
		#			* WAIT! we don't want to expand wikipedia pages forever!
		#			* So we have recursion_count to tell us when to stop
		#			* This bit is fussy, and you can easily get in an endless loop
		#			
		w = self.get_interesting_links()
		if randomize_links == True:
			random.shuffle(w)
		otherlinks = w[0:links_per_article]
		for ID in otherlinks:
			if ID not in self.page_directory:
				wp = WikiPage(self.page_directory, ID)
				if recursion_count > 0:
					wp.load_links(recursion_count = recursion_count - 1, links_per_article=links_per_article )		
		return None


	def print_summary(self):
		""" Print a summary of this page """
		print(f"{self.page_id} (title:'{self.title}')")
		print(f"\tURL:       {self.url}")
		print(f"\tLast edit: {self.last_edit}")
		print(f"\tWordcount: {self.wordcount}")
		link_text = ",".join(self.wiki_links[:5]) + "..." + ",".join(self.wiki_links[-5:])
		print(f"\t{len(self.wiki_links)} links:     {link_text}")

	def find_path(self, current_path, query_id, max_path_length=4):
		"""
		If this page has a path to this id, return the path
		This solves the wiki game "Six degrees of Wikipedia"
		https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia

		Parameters: 
			current_path (list of str): The path we have taken so far, we need this 
				so we can see if we in a loop 
				(ie "Illinois -> US State -> Indiana -> Illinois -> US State".....) 
			query_id (str): The page id we are trying to get to
			max_path_length: the longest path we are allowed to take 
				(prevents unproductively long searches)
		Returns: 
			list of str: the path of wiki page ids that take us from the 
				start to the query_id, if a path exists from this page
			None: if there is no path found
		"""

		# Add ourselves to the current path 
		# Note that this makes a *copy* of the path
		next_path = current_path + [self.page_id]

		if self.page_id in current_path:
			# We've been here before, no loops!
			# So stop here
			return None

		if self.page_id == query_id:
			return next_path

		# Search all subpages
		for wiki_id in self.wiki_links:

			# Is the query one of our direct links?
			if wiki_id == query_id:
				return next_path + [wiki_id]

			# If this next page is in our directory
			# AND we still have path length left, 
			# RECURSE to search this page next
			# and if it finds a successful path return it
			if wiki_id in self.page_directory and len(current_path) < max_path_length:
				subpage = self.page_directory[wiki_id]
				potential_path = subpage.find_path(next_path, query_id, max_path_length)
				if potential_path:
					return potential_path
					
		# If we get here, we have not found a path
		return None

	#---------------------------
	# Functions to display a nice tree diagram

	def display_tree(self):
		print(f"\nTree diagram, starting at page '{self.title}'")
		tree = Tree()

		tree.create_node(self.page_id, self.page_id)
		self.add_to_tree(tree)
		tree.show()


	def add_to_tree(self, tree):
		
		max_links_to_display = 20

		# Definitely show any links we have loaded, 
		# otherwise just the first and last N
		for link_id in self.wiki_links[0:max_links_to_display]:
			
			# Add this link to our tree, if it's not already in the tree
			# (no loops allowed!)
			if not tree.contains(link_id):


				tree.create_node(link_id, link_id, parent=self.page_id)
				if link_id in self.page_directory:	
					self.page_directory[link_id].add_to_tree(tree)
				

if __name__ == "__main__":

	test_song_articles = ["Airplane_Pt._2", "Thank_U,_Next_(song)", "Montero_(Call_Me_by_Your_Name)", "Savage_Love_(Laxed_%E2%80%93_Siren_Beat)"]
	test_interesting_articles = ["Trojan_Room_coffee_pot", "Rubber_duck_debugging", "IP_over_Avian_Carriers", "Scunthorpe_problem", "The_Complexity_of_Songs", "Illegal_number", "MONIAC"]
	test_chicago_articles = ["Max_Headroom_signal_hijacking", "Raising_of_Chicago", "Flag_of_Chicago", "Great_Chicago_Fire", "List_of_nicknames_for_Chicago", "List_of_songs_about_Chicago"]

	# for url in test_song_articles:
	# 	print(f"{url} -> {url_to_id(url)}")

	
	# Load a Wikipedia article (you can change this to look at any article)
	# (Comment out the asserts if you want to test other articles)
	test_url = "https://en.wikipedia.org/wiki/Cat"
	# test_url = "https://en.wikipedia.org/wiki/" + test_interesting_articles[0] # Try loading "Rubber_duck_debugging"

	
	# Load the HTML from either online, or from a cache 
	# (notice what happens when you run it multiple times, 
	# and notice the "cache" folder that appears in your assignment)
	# You can also print out the debug information when the page loads
	test_html = load_url_politely(test_url, print_debug=True)
	test_soup = BeautifulSoup(test_html, features="html.parser")
		
	# This will print the whole page (a lot!)
	
	# This will print just the *plaintext* (without all the <> markup)
	# print(test_soup.text)

	#------------------------------------------------------------------
	# Scraping basic information out of Beautiful Soup

	# Test Tasks 0, 1, 2

	test_count = get_wordcount(test_soup)
	test_title = get_title(test_soup)
	test_edit = get_last_edit(test_soup)

	print("-"*50 +  "\nBASIC PAGE INFO:")
	print(f"\tURL =		'{test_url}'")
	print(f"\tWordcount =	'{test_count}'")
	print(f"\tTitle =		'{test_title}'")
	print(f"\tLast edit =	'{test_edit}'")

	assert test_title == "Cat", f"Expecting title 'Cat', your answer: '{test_title}'"
	expected_cat_count = 16378
	expected_cat_edit = "8 November 2022"
	if test_count != expected_cat_count:
		print(f"*** POSSIBLE ERROR: Don't worry if this isn't exact (articles get edited), but your word count is {test_count} and we expected something close to {expected_cat_count}")
	if test_edit != expected_cat_edit:
		print(f"*** POSSIBLE ERROR: Don't worry if this isn't exact (articles get edited), but your edit date is {test_edit} and we expected something close to {expected_cat_edit}")
	
	# #------------------------------------------------------------------
	# # Getting and processing links


	# Get all the links in the Cat article
	# Notice that there are a bunch of different kinds of links here

	# Test Tasks 3
	test_links = get_all_links(test_soup)
	print("-"*50 +  "\nLINK DATA:")
	print(f"Found {len(test_links)} links in {test_title}")
	print("\tincluding", test_links[0:10]) # You can change this "5" to see more than 5 links

	# Test Tasks 4
	wiki_ids = get_all_wiki_link_ids(test_soup)
	print(f"Found {len(wiki_ids)} links to other Wiki articles in {test_title}")
	print("\tincluding", wiki_ids[0:10])

	#------
	# Interesting data science:
	# Have a lot of something? Here are a few ways to look at large lists of information
	
	# Print all of the wiki ids, sorted alphabetically ("sorted"), with duplicates removed ("set")
	# alphabetical_wiki_ids = sorted(set(wiki_ids))
	# print(",".join(alphabetical_wiki_ids))

	# How many times was each link referenced? Make a counter! 
	# https://realpython.com/python-counter/
	counts = Counter(wiki_ids)

	# Just print all the counts
	pprint(counts)

	# Calculate how many articles are referenced 1, 2, 3, 4... times in this article
	# What is the most common outgoing link from the Cat article?
	for i in range(1,7):
		wiki_ids_with_count = [id for (id,count) in counts.items() if count == i]
		print(f"Seen {i} times: {len(wiki_ids_with_count)} total",  wiki_ids_with_count[0:5])

	assert "Purring" in wiki_ids, "Should have found a link to the wiki page for 'Purring'"
	assert "Kneading_(cats)" in wiki_ids, "Should have found a link to the wiki page for 'Kneading_(cats)'"
	assert not "Category:Cats" in wiki_ids, "Remember to remove links with a ':'"
	assert not "Red_panda#Taxonomy" in wiki_ids, "Remember to remove links with a '#'"
	
	#------------------------------------------------------------------
	# Putting information into a WikiPage class instance
	# so we can do advanced queries on it

	# Like in the last assignment, we have a data structure to hold everything
	# 	But this time its a *dictionary* instead of a list
	# 	So that we can easily look pages up by their id: 
	# 	e.g "page_directory['Cat']", page_directory['Montero_(Call_Me_by_Your_Name)']"
	page_directory = {}

	test_page = WikiPage(page_directory, "Evanston,_Illinois")

	# # Test Task 5

	assert test_page.title == "Evanston, Illinois"
	assert isinstance(test_page.soup, BeautifulSoup), "Did you save the BeautifulSoup object?"
	assert isinstance(test_page.wordcount, int), f"Wordcound should be an integer, was {test_page.wordcount}"
	assert isinstance(test_page.last_edit, str), f"Last edit should be a date (str), was {test_page.last_edit}"
	assert "Northwestern_University" in test_page.wiki_links, "Northwestern should be one of the wiki links of the article on Evanston"
	
	assert isinstance(test_page.page_directory, dict), "Did you store page_directory as a property on the WikiPage instance?" 
	assert page_directory["Evanston,_Illinois"] == test_page, "Did you store the WikiPage instance in the directory so we can access it later?" 

	# # Load several pages
	for wiki_id in test_interesting_articles:
		new_page = WikiPage(page_directory, wiki_id)

	# # Test Task 6

	print("-"*50 +  "\nSHORTEST AND OLDEST PAGES:")
	
	
	# Printing out each page and its length 
	# (may be useful to both debug *and* program Task 6!)
	# No asserts, because these might change, but hopefully this makes the right answer obvious
	for page_id in page_directory:
		page = page_directory[page_id]
		print(f"\t{page_id:30} {page.last_edit:20} {page.wordcount} words") 
	
	shortest = get_shortest_page(page_directory)
	oldest = get_oldest_page(page_directory)
	print("Shortest article: ", shortest.title, shortest.wordcount)
	print("Oldest article: ", oldest.title, oldest.last_edit)


	# ------------------------------------------------------------------
	#Test Task 7
	#Load links *recursively*

	page_directory = {}
	cat_page = WikiPage(page_directory, "Cat")

	# Try without recursion
	print("\n-- Load NON-RECURSIVELY --")
	cat_page.load_links(links_per_article=5, recursion_count=0)
	print("All loaded pages ", page_directory.keys())
	
	# Show a tree visualization of all links accessible from this page 
	# (Wikipedia isn't actually a tree, there are also loops, but we don't visualize those here)
	print("\n-- Load RECURSIVELY --")
	page_directory = {}
	cat_page = WikiPage(page_directory, "Cat")

	# cat_page.display_tree()
	# assert "Conservation_status" in page_directory, "If it loaded the first 5 links from Cat, 'Conservation_status' should be in the directory"
	
	# Try with more recursion, but fewer links:
	# this will get further away from the original article
	cat_page.load_links(links_per_article=2, recursion_count=3)
	# cat_page.display_tree()
	print("All loaded pages ", sorted(page_directory.keys()))
	# assert "Felidae" in page_directory, "If it loaded the links 3 links deep from Cat, 'Felidae' should be in the directory"
	


	# ------------------------------------------------------------------
	# Testing it out
	# Play Six Degrees of Wikipedia using find_path
	# You don't have to edit find_path, but read it to see 
	# how we can *recursively* search a tree or graph structure 
	# to build up a path between two nodes
	# (https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia)
	# https://www.sixdegreesofwikipedia.com/
	# If you time out, you have made too many requests, so wait a minute and run it again
	# Or reduce the number of pages you are loading

	# Try loading different pages, and find unexpected paths between topics

	# Make sure we have some cat pages loaded
	cat_page = WikiPage(page_directory, "Cat")
	cat_page.load_links(links_per_article=4, recursion_count=2)

	# Lets load two more sets of pages so we have more pages to play with
	evanston_page = WikiPage(page_directory, "Evanston,_Illinois")
	evanston_page.load_links(links_per_article=4, recursion_count=2)
	
	cs_page = WikiPage(page_directory, "Computer_science")
	cs_page.load_links(links_per_article=4, recursion_count=2)
	cs_page.display_tree()

	print("Total pages loaded", ", ".join(page_directory.keys()))

	
	# What other paths can we find with only 80 or so pages loaded?
	# Some of these have no path found, but can you find a path if you load more pages?
	# What other connections can you find?
	
	print(f"Path found from Cat to Evanston,_Illinois", page_directory["Cat"].find_path([], "Evanston,_Illinois"))
	print(f"Path found from Cat to Dinosaur", page_directory["Cat"].find_path([], "Dinosaur"))
	print(f"Path found from Cat to Computer_science", page_directory["Cat"].find_path([], "Computer_science"))
	print(f"Path found from Evanston,_Illinois to Cat", page_directory["Evanston,_Illinois"].find_path([], "Cat"))
	print(f"Path found from Cat to Arabic", page_directory["Cat"].find_path([], "Arabic"))
	print(f"Path found from Computer_science to Half-Life_(series)", page_directory["Computer_science"].find_path([], "Half-Life_(series)"))
	print(f"Path found from Computer_science to Chicago", page_directory["Computer_science"].find_path([], "Chicago"))
	print(f"Path found from Alphabet to Automation", page_directory["Alphabet"].find_path([], "Automation"))


	
