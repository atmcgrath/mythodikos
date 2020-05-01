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

def get_section(line):
	cite_list = []
	for parent in line.parents:
		if parent.name == 'div':
			if parent.attrs['type'] == 'textpart':
				try:
					cite_list.append(parent.attrs['subtype']+parent.attrs['n']) # printing subtype tells us exactly which parts of the citation are being returned -- comment out later
				except KeyError:
					continue
			else: continue
		elif 'div' in parent.name:
			try:
				cite_list.append(parent.attrs['type']+parent.attrs['n'])
			except KeyError:
				continue
	cite_list.reverse() # make order: book,chapter,section
	citation = '.'.join(cite_list) # make format: book.chapter.section
	return citation

def get_linenum(line): # separated from get_section to test
	textchunk = line.parent # m.parent == the exact section of .xml text in which the match is found (could be a paragraph or a line)
	line_num = ''
	for chunk in textchunk:
		if textchunk.name == 'l' or 'lb': # for line number of match
			try:
				line_num = textchunk.name + ' ' + textchunk['n']
			except KeyError:
				continue
		else:
			continue
	return line_num

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
outfile = "/Users/stellafritzell/mythodikos/corpus-test-5-01.csv"

persondict = {
			'Atalanta': [r'\bἈταλάντ'], 
			'Arion': [r'\bἈρίων', r'\bἈρίον']
			} # Compile in reference to LIMC

placedict = {
			'Arcadia': [r'\bἈρκαδ'], #need for lowercase reg-ex as well?
			#'Athens': [r''],
			'Boeotia': [r'\bΒοιωτ', r'\bΒοιῳτ', r'\bΒοϊωτ', r'\bΒοέκ', r'\bβοεκ'],
			#'Calydon': [r''],
			#'Colchis': [r''],
			#'Corinth': [r''],
			#'Lacedaemon': [r''],
			#'Lesbos': [r''],
			#'Lycaeus': [r''],
			#'Mainalos': [r''],
			#'Methymna': [r''],
			#'Parthenion': [r''],
			#'Taenarum': [r''],
			#'Tarentum': [r''],
			#'Tegea': [r''],
			'Thebes': [r'\bΘήβ', r'\bΘῆβ']
			} # Compiled in reference to OCD "Ancient Geography Entries" ; as alternative, compile in reference to Barinton Atlas of the Ancient World

# build .csv with desired metadata as column headers
with open(outfile, 'w') as z:
	f = csv.writer(z)
	f.writerow(['person', 'place', 'title', 'author', 'section', 'line', 'context', 'length', 'filename'])

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

					for person in persondict:
						pers = persondict[person] # value list for each key
						for p in pers: # each regex value in value lists
							pers_matches = soup.find_all(string=re.compile(p)) 

							for match1 in pers_matches: # match = entire matching string
								context = match1.replace('\n', '') # strips newline characters
								
								for place in placedict: #this chunk essentially runs another full corpus search - how to use for just results of 'person' search?
									geo = placedict[place]
									for g in geo:
										geo_matches = soup.find_all(string=re.compile(g))
										
										for match2 in geo_matches:
											if match2 in context:
												try:
													section = get_section(match1) # applies citation formula to each match
													line = get_linenum(match1)
													length = len(context) # number of characters in context
													f.writerow([person, place, text_title, text_author, section, line, context, length, file]) #write defined variables for each match to .csv
												except KeyError:
													continue
											else:
												continue

								'''
								PSEUDO CODE FOR MATCH PAIRS:
								for match context
									if match context contains value from placedict
										try: get citation info (f.writerow(...))
										except:
											continue
									else:
										continue
								'''
								
								# context = get_context(m)
