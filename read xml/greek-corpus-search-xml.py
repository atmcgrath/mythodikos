#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project:
1. iterates through corpus
1. opens file, parses file, finds pattern matches with regex values & keys in a dictionary
2. for each match: records latinized name (key), title & author of text (needs some refinement), citation (with issues), text context (with issues), and file name
3. writes information to .csv

Next Steps:
1. refine 'context' criteria
1. clean up citation extraction, author and title
2. compile place-name search terms using place_names.csv (has nominative greek & latinized forms, & Pleiades id) and regex (for both noun & adjective forms)
3. find word matches with placenames

*** From the Perseus DL github: "if a file ends in "1," it is likely this file is not CTS (Cannonical Text Services) compliant" -- i.e. it is probably not encoded with the same consistency of the files that are CTS compliant

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
	sections = [parent.attrs for parent in line.parents if parent.name == 'div'] # Stephanus numbers (i.e. Plato) would be more accurate in some cases, but these are 'milestone' parents and non-priority
	for s in sections: # for attritubutes of 'div'
		if s['type'] == 'textpart': # only look at textpart 'div'
			try:
				cite_list.append(s['subtype']+s['n']) #printing subtype tells us exactly which parts of the citation are being returned -- comment out later
			except KeyError:
				continue
		elif s['type'] == 'poem': # to get the number for a poem in an author's work
			try:
				cite_list.append(s['type']+s['n'])
			except KeyError:
				continue
	cite_list.reverse() # make order book - chapter - section

	textchunk = line.parent # m.parent == the exact section of .xml text in which the match is found (could be a paragraph or a line)
	for chunk in textchunk:
		if textchunk.name == 'l': # for line number of match
			try:
				cite_list.append('line'+textchunk['n'])
			except KeyError:
				continue
		elif textchunk.name == 'lb': #this should account for <lb n='#' rend="displayNum"/> line citation in Callimachus files (tlg0533.tlg017), but does not.  Why?
			try:
				cite_list.append('line'+textchunk['n'])
			except KeyError:
				continue

			# some files are encoded with line numbers for every 5 lines of text.  How to address this?

	citation = '.'.join(cite_list) # make citation format book.chapter.section.line
	return citation

"""
def get_context(line):
	context = []
	if m.parent.t == 'l': #or <lb/>
		prev_line = matchchunk.previous_sibling.previous_sibling.string
		next_line = matchchunk.next_sibling.next_sibling.string
		context = prev_line + ' ' + m + ' ' + next_line # this returns text as a full string, rather than as three lists
	elif m.parent.t == 'p': # for paragraphs consider using cltk / nltk sentence tokenize to return the match sentence
		context = .... # is there a way to have the program return the text surrounding the match up to the nearest punctuation mark?
"""

# =====================================================================
# Program
# =====================================================================

greekcorpusdir = "/Users/stellafritzell/mythodikos/canonical-greekLit-master"
outfile = "/Users/stellafritzell/mythodikos/corpus-test-4-21.csv"

persondict = {'Atalanta': [r'\bἈταλάντ'],
			'Arion': [r'\bἈρίων', r'\bἈρίον']
			} # Compile in reference to LIMC

placedict = {} # Compile in reference to Barinton Atlas of the Ancient World

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
						terms = persondict[key] # value list for each key
						for t in terms: # each regex value in value lists
							matches = soup.find_all(string=re.compile(t))

							for m in matches: # m = entire matching string
								citation = get_citation(m) # applies citation formula to each match
								# context = get_context(m)

								f.writerow([key, text_title, text_author, citation, t, m, file]) #write defined variables for each match to .csv
