#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:41:03 2020

Code for mythodikos project
1. Iterates through corpus
2. Opens text file, reads file, turns raw text into nltk text object
3. Searches a text for keyword and returns a slice 5 words before and after keyword

Next steps:
- Find word matches with dictionary list (placenames)
- Write matches to csv with filename
- Turn chunks into functions

NB: I made some untested changes to clean this up 1/10

@author: atmcgrath
"""

import nltk # natural language toolkit - http://www.nltk.org/
# import re
# import pprint
from nltk import word_tokenize
# import os

# =============================================================================
# Iterates through files and subfolders in the directory contaning the corpus
# =============================================================================

"""
corpusdir = "~/cltk_data/latin/text/latin_text_latin_library"

for root, dirs, files in os.walk(corpusdir):
    for filename in files:
        infile = root + '/' + filename
# commented out while testing search functions on single text
"""

# =============================================================================
# Processes single text file into nltk text object (a list of words, among other things)
# =============================================================================

infile = "~/cltk_data/latin/text/latin_text_latin_library/agnes.txt"

raw = open(infile).read() # stores contents of file
tokens = word_tokenize(raw) # tokenizes raw text (list of words)
text = nltk.Text(tokens) # creates a Text object for nltk functions

keyword = "semper" # in place of a name, since I don't read latin

# =============================================================================
# Getting slices of words around keyword
# =============================================================================

# Method 1) - index all instances, create list, locate index + or - 5 words

if keyword in text:
    matchlist = [i for i, item in enumerate(text) if item == keyword]
# Creates a list comprehension that records the index value of each occurrence of keyword 'semper'

    results = [] # create list to store text segments
    for instance in matchlist: # Iterates through indexes
        first = instance - 6 # Creates variable for index 5 words before occurence
        last = instance + 6 # ditto 5 words after
        result = text[first:last] # creates a list for that 10-word slice
        results.append(result) # appends that list to 'results'

    for r in results: # for testing purposes: display results
        print(r)
else: continue

"""
# this worked but there may be a better way
# stack exchange turned this up, but it didn't work https://simply-python.com/2014/03/14/saving-output-of-nltk-text-concordance/

"""
