#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project:
1. iterates through corpus
1. opens file, parses file, finds pattern matches with regex values & keys in a dictionary
2. for each match: records latinized name (key), title & author of text, citation (with issues), text context (with issues), and file name
3. writes information to .csv

Next Steps:
1. refine 'context' criteria
1. clean up citation extraction
2. compile place-name search terms using place_names.csv (has nominative greek & latinized forms, & Pleiades id) and regex (for both noun & adjective forms)
3. find word matches with placenames


@author: sfritzell
adapted from: search-xml-greek.py
"""

# =====================================================================
# Imports & Modules
# =====================================================================

import os # to search file directory
import fnmatch # to specify files
import re # to use regex functions
from bs4 import BeautifulSoup # to read xml files
import csv
# import nltk
# from nltk import word_tokenize # to retun a smaller word context for mathces in paragraphs

# =====================================================================
# Functions
# =====================================================================

def get_citation(line):
	cite_list = []
	sections = [parent.attrs for parent in m.parents if parent.name == 'div'] # Stephanus numbers (i.e. Plato) would be more accurate in some cases, but these are 'milestone' parents and non-priority
	for s in sections: # for each 'div' attributes dictionary
		if s['type'] == 'textpart' or 'chapter': # this is also returning 'div' that have an 'edition' attribute, where 'n' = the tlg/perseus edition/catalogue numbers (not needed)
			try:
				cite_list.append(s['n']) # return the number of that text part; PROBLEM: not all 'textpart' divs seem to have numbers ???
			except:
				continue
	cite_list.reverse()
	line = [parent.attrs for parent in m.parent if parent.name == 'l']
	for l in line:
		cite_list.append(l['n'])
	citation = '.'.join(cite_list)
	return citation

# =====================================================================
# Program
# =====================================================================

greekcorpusdir = "/Users/stellafritzell/mythodikos/canonical-greekLit-master"
outfile = "/Users/stellafritzell/mythodikos/corpus-test-2-26.csv"

persondict = {'Atalanta': [r'\bἈταλάντ'], 'Arion': [r'\bἈρίων', r'\bἈρίον']}

"""
for key in persondict:
	terms = persondict[key] # returns values as lists
	for t in terms:
		print(t) # returns regex strings
"""
# build .csv with desired metadata as column headers
with open(outfile, 'w') as z:
	f = csv.writer(z)
	f.writerow(['person', 'title', 'author', 'citation', 'match', 'context', 'filename'])

	for root, dirs, files in os.walk(greekcorpusdir):
		for file in files:
			if fnmatch.fnmatch(file, '*grc*.xml'):
				infile = root+'/'+str(file) # specifices greek text files for search
				
				with open(infile) as x:
					soup = BeautifulSoup(x, features='lxml')

					text_title = soup.title.string
					if soup.author:
						text_author = soup.author.string
					else: text_author = ''

					for key in persondict:
						terms = persondict[key] # values of dictionary keys in list form
						for t in terms: # each item of the value lists
							matches = soup.find_all(string=re.compile(t)) 

							for m in matches: # m = occurance of matching string
								matchchunk = m.parent # matchchunk represents the line containing m
								
								"""
								context = []
								if m.parent.t == 'l':
									prev_line = matchchunk.previous_sibling.previous_sibling.string
									next_line = matchchunk.next_sibling.next_sibling.string
									context = prev_line + ' ' + m + ' ' + next_line # this returns text as a full string, rather than as three lists
								elif m.parent.t == 'p': # for paragraphs consider using cltk / nltk sentence tokenize to return the match sentence
									context = m
								"""

								citation = get_citation(matchchunk) # + '.' + linenumber # this appends line number to the section numbers in standard format

								f.writerow([key, text_title, text_author, citation, t, m, file]) # maybe write function for differnt types of matchchunk context?

