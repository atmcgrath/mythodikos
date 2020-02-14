#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project:
1. iterates through corpus
1. opens file, parses file, finds pattern matches with keys from a dictionary ({name varient: latinzied name})
2. for each key match: records latinized name, title & author of text, citation, text context (text line, one line before and after), and file name
3. writes information to .csv

Next Steps:
1. clean up search problems (duplicate results, 'textparts' without 'n', 'l' and 'p' contexts)
2. compile place-name search terms using place_names.csv (has nominative greek & latinized forms, & Pleiades id) and lemmatized search and/or regex (for adjectives)
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
import nltk
from nltk import word_tokenize # to retun a smaller word context for mathces in paragraphs

# =====================================================================
# Functions
# =====================================================================

def get_citation(line):
	cite_list = []
	sections = [parent.attrs for parent in m.parents if parent.name == 'div'] # Stephanus numbers (i.e. Plato) would be more accurate in some cases, but there are 'milestone' parents
	for s in sections: # for each 'div' attributes dictionary
		if s['type'] == 'textpart': # for any 'div' demarkating a section of text
			cite_list.append(s['n']) # return the number of that text part; PROBLEM: not all 'textpart' divs seem to have numbers ???
		elif s['type'] == 'chapter':
			cite_list.append(s['n'])
		else:
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
outfile = "/Users/stellafritzell/mythodikos/corpus-test-2-14.csv"

persondict = {
	'Ἀταλάντη': 'Atalanta', 'Ἀταλάντης': 'Atalanta', 'Ἀταλάντα': 'Atalanta', 'Ἀταλάνται': 'Atalanta', 'Ἀταλάνταις': 'Atalanta', 'Ἀταλάντας': 'Atalanta', 'Ἀταλάντῃ': 'Atalanta', 'Ἀταλάντην': 'Atalanta',
	'Ἀρίων': 'Arion', 'Ἀρίωνι': 'Arion', 'Ἀρίωνα': 'Arion', 'Ἀρίωνος': 'Arion', 'Ἀρίον': 'Arion', 'Ἀρίονος': 'Arion', 'Ἀρίονα': 'Arion', 'Ἀρίονι': 'Arion'
	}

# build .csv with desired metadata as column headers
with open(outfile, 'w') as z:
	f = csv.writer(z)
	f.writerow(['person', 'title', 'author', 'citation', 'context', 'filename'])

	for root, dirs, files in os.walk(greekcorpusdir):
		for file in files:
			if fnmatch.fnmatch(file, '*grc*.xml'):
				infile = root+'/'+str(file) # specifices greek text files for search
				
				with open(infile) as x:
					soup = BeautifulSoup(x, features='lxml')

					text_title = soup.title.string
					text_author = soup.author.string

					for key in persondict:
						name = persondict[key]
						matches = soup.find_all(string=re.compile(key))

						for m in matches: # m = occurance of matching string
							matchchunk = m.parent # matchchunk represents the line containing m
							"""
							context = []
							if m.parent.name == 'l':
								prev_line = matchchunk.previous_sibling.previous_sibling.string
								next_line = matchchunk.next_sibling.next_sibling.string
								context = prev_line + ' ' + m + ' ' + next_line # this returns text as a full string, rather than as three lists
							elif m.parent.name == 'p':
								context = m
							"""	
							citation = get_citation(matchchunk) # + '.' + linenumber # this appends line number to the section numbers in standard format

							f.writerow([name, text_title, text_author, citation, matchchunk, infile]) # maybe write function for differnt types of matchchunk context?
