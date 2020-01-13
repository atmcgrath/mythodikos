#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Monday, Jan 13 2020

Testing code for mythodikos project. 
Canonical version is corpus-word-search.py   


@author: atmcgrath
"""

import nltk # natural language toolkit - http://www.nltk.org/
# import re
# import pprint
from nltk import word_tokenize
import os
import csv

# =============================================================================
# Functions
# =============================================================================

def is_match(wordlist, text_obj):
    matches = 0
    for word in wordlist:
        if word in text_obj:
            match = 1
        else:
            match = 0
        matches += match
    if matches > 0:
        return True
    else:
        return False
        
def word_matches(wordlist, text_obj):
    matches = []
    for word in wordlist:
        if word in text_obj:
            matches.append(word)
        else:
            continue
    return matches   

# =============================================================================
# Iterates through files and subfolders in the directory contaning the corpus
# =============================================================================

#outfile = "/Users/amcgrath1/classics/mytho-test-1-13.csv"

#f = csv.writer(open(outfile, 'w'))
#f.writerow(['filename', 'keyword', 'index', 'context'])

keyword = "semper" # in place of a name, since I don't read latin

keywords = ['semper', 'iulius', 'julius']

corpusdir = "/Users/amcgrath1/cltk_data/latin/text/latin_text_latin_library"

"""

for root, dirs, files in os.walk(corpusdir):
    for filename in files:
        infile = root + '/' + filename
"""    
# =============================================================================
# Processes single text file into nltk text object (a list of words, among other things)
# =============================================================================

# infile = "/Users/amcgrath1/cltk_data/latin/text/latin_text_latin_library/agnes.txt"
"""
        with open(infile) as fp:
            raw = fp.read() # stores contents of file
            if is_match(keywords, raw) == True:
                tokens = word_tokenize(raw) # tokenizes raw text (list of words)
                text = nltk.Text(tokens) # creates a Text object for nltk functions
                for counter, value in enumerate(text):
                    for key in keywords:
                        if value == key:
                            print(filename, counter, value)
                        else: 
                            continue
            else:
                print(filename + " no match")
"""
for root, dirs, files in os.walk(corpusdir):
    for filename in files:
        infile = root + '/' + filename
        with open(infile) as fp:
            raw = fp.read() # stores contents of file
            matches = word_matches(keywords, raw)
            if len(matches) == 0:
                print(filename + " no match")
            else: 
                tokens = word_tokenize(raw) # tokenizes raw text (list of words)
                text = nltk.Text(tokens) # creates a Text object for nltk functions
                for counter, value in enumerate(text):
                    for key in matches:
                        if value == key:
                            print(filename, counter, value)
                        else: 
                            continue

        
# =============================================================================
# Getting slices of words around keyword
# =============================================================================

"""
# Method 1) - index all instances, create list, locate index + or - 5 words

            if keywords[0] or keywords[1] or keywords[2] in text
            for key in keywords:
                if key in text:
                    matchlist = [i for i, item in enumerate(text) if item == key]
# Creates a list comprehension that records the index value of each occurrence of keyword 'semper'

 #       results = [] # create list to store text segments
                    for instance in matchlist: # Iterates through indexes
                        first = instance - 6 # Creates variable for index 5 words before occurence
                        last = instance + 6 # ditto 5 words after
                        result = text[first:last] # creates a list for that 10-word slice
            
  #                  f.writerow([filename, key, instance, result])
                
                else:
                    continue        



# this worked but there may be a better way
# stack exchange turned this up, but it didn't work https://simply-python.com/2014/03/14/saving-output-of-nltk-text-concordance/

"""
