#!/usr/bin/env python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos projcect:
1. Open file, read file, find matches
2. Gets line number for match 


Next Steps:
1. remove accents (resource: https://github.com/jtauber/greek-accentuation)
2. write results to csv
3. return three lines around keyword match using TokenizeSentence (cltk) or soup.next_sibling / .previous_sibling
4. find word matches with placenames
5. use regex for keyword variations OR find a way to search for lemmas of keywords (resource: http://docs.cltk.org/en/latest/greek.html#lemmatization)
6. turn chunks of code into functions

"""

# =====================================================================
# Imports
# =====================================================================

from bs4 import BeautifulSoup

# import nltk # natural language toolkit - http://www.nltk.org/
# from nltk import word_tokenize

import re

# import os
# import csv

# =====================================================================
# Functions
# =====================================================================



# =====================================================================
# Program
# =====================================================================

infile = "/Users/stellafritzell/mythodikos/canonical-greekLit-master/data/tlg0001/tlg001/tlg0001.tlg001.perseus-grc2.xml"

# outfile = "/Users/stellafritzell/mythodikos/test-1-24.csv"
# f = csv.writer(open(outfile), 'w')
# f.writerow(['keyword', 'citation', 'content', 'filename'])

""" 
desired xml metadata:
Author, Work:  <teiHeader>
								<fileDesc>
									<titleStmt>
										<title>
										<author>
			Text Citation: <text>
								<body>
									<div>
										<div subtype='book' n='1'>
											<l n='1'>
			Context: print line above and below keyword (.next_sibling & .previous_sibling)
"""

personlist = ['Ἀμφιδάμας', 'Μελέαγρος', 'Ζήτης']

soup = BeautifulSoup(open(infile), features="lxml")

# returns each line (reads as string) for keyword match, does not work for list
# abbreviation: soup("a") = soup.find_all("a")
matches = soup.find_all(string=re.compile('Ἀμφιδάμας'))
for m in matches:
    print(m) # prints line with match
    print(m.parent['n']) # prints line number
    print(m.parent.previous_sibling.previous_sibling.string) # should be previous line but still working this out
    
# .find_parents for each returned string might be able to return some citation metadata

# once parents of sting(s) are indentified, modify this to return metadata citation?
for tag in soup.find_all('title'):
	print(tag.sourceline, tag.sourcepos, tag.string)

