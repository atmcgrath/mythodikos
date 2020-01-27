#!/usr/bin/env python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos projcect: Greek search
1. Open xml, parse xml, find pattern matches for a keyword list (personlist)
2. For each match: records line number and line text
3. For each match: records text section info
4. For each match: gets title and author of text
5. For each match: returns one line before and after matching line, as list
6. Wites to .csv

Next Steps:
1. use regex for keyword variations OR find a way to search for lemmas of keywords (resource: http://docs.cltk.org/en/latest/greek.html#lemmatization)
2. remove accents (resource: https://github.com/jtauber/greek-accentuation)
3. find word matches with placenames
4. turn chunks of code into functions

@author: sfritzell
informed by search-xml-latin.py
"""

# =====================================================================
# Imports
# =====================================================================

from bs4 import BeautifulSoup

# import nltk # natural language toolkit - http://www.nltk.org/
# from nltk import word_tokenize

import re

# import os
import csv

# =====================================================================
# Functions
# =====================================================================

# finds text section information, needs to be tested robustly on corpus
def get_citation(line):
	grups = [par.atts for par in m.parents if par.name == 'div']
	cite_list = []
	for g in grups:
		try:
			cit = g['subtype'] + '' + g['n']
			cite_list.append(cit)
		except:
			continue
	cite_list.reverse()
	citation = '; '.join(cite_list)
	return citation
""" 
this function pulls some of the information when tested on its own (using print) following the code block for write.csv
with references to the funciton itself commented out.
When run as a function, however, it does not print to .csv
"""  

# =====================================================================
# Program
# =====================================================================

infile = "/Users/stellafritzell/mythodikos/canonical-greekLit-master/data/tlg0001/tlg001/tlg0001.tlg001.perseus-grc2.xml"

outfile = "/Users/stellafritzell/mythodikos/test-1-27.csv"

personlist = ['Ἀμφιδάμας', 'Μελέαγρος', 'Ζήτης']

soup = BeautifulSoup(open(infile), features="lxml")

# build .csv with desired metadata as column headers
with open(outfile, 'w') as z:
	f = csv.writer(z)
	f.writerow(['title', 'author', 'person', 'section', 'line number', 'context'
		#, 'filename'
		])

	text_title = soup.title.string
	text_author = soup.author.string

	# creates list of string matches
	for person in personlist:
		matches = soup.find_all(string=re.compile(person))

		for m in matches: # m = occurance of matching string
			linematch = m.parent # linematch represents the line containing m
			linenumber = m.parent['n'] # line number attribute of line match
			prev_line = linematch.previous_sibling.previous_sibling.string
			next_line = linematch.next_sibling.next_sibling.string
			context = [prev_line, m, next_line]
			citation = get_citation(linematch) # see issue mentioned in function comment

			f.writerow([text_title, text_author, person, citation, linenumber, context])
