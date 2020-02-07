#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:41:03 2020

Code for mythodikos project
1. Iterates through corpus
2. Opens text file, reads file, checks for matches
3. Turns raw text into nltk text object
4. Returns a slice 5 words before and after each keyword match
5. Writes results to a csv

Next steps 1/13
- Find word matches with dictionary list (placenames)
- Beautiful soup for xml searching
- Regex instead of word lists?
- Turn chunks into functions? 
- Resolve encoding error: 
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xdf in position 15: invalid continuation byte    


@author: atmcgrath
"""

import nltk # natural language toolkit - http://www.nltk.org/
# import re
# import pprint ?
from nltk import word_tokenize
import os
import csv

# =============================================================================
# Functions
# =============================================================================

# Determines whether a text contains any of the keywords and returns a list of matching keywords

def word_matches(wordlist, text_obj):
    matches = []
    for word in wordlist:
        if word in text_obj:
            matches.append(word)
        else:
            continue
    return matches


# =============================================================================
# Program
# =============================================================================

outfile = "/Users/amcgrath1/classics/mytho-test-1-13-new.csv"

f = csv.writer(open(outfile, 'w'))
f.writerow(['filename', 'keyword', 'index', 'context'])

keyword = "semper" # in place of a name, since I don't read latin

keywords = ['semper', 'iulius', 'julius']

corpusdir = "/Users/amcgrath1/cltk_data/latin/text/latin_text_latin_library"

#  Iterates through files and subfolders in the directory contaning the corpus
for root, dirs, files in os.walk(corpusdir):
    for filename in files:
        infile = root + '/' + filename

# infile = "/Users/amcgrath1/cltk_data/latin/text/latin_text_latin_library/agnes.txt"

        with open(infile) as fp:
            raw = fp.read() # stores contents of file
            matches = word_matches(keywords, raw) #searches file contents for keyword matches
            if len(matches) == 0: # If no matches exist, move on to next file
                continue 
            else: # If matches exist
                tokens = word_tokenize(raw) # tokenizes raw text
                text = nltk.Text(tokens) # creates a Text object for nltk functions
                for counter, value, in enumerate(text): # Identifies index numbers for each word
                    for key in matches: # Iterates through present matching keywords
                        if value == key: # For each match, creates 10-word slice around keyword
                            first = counter - 6 
                            last = counter + 6
                            result = text[first:last]
                            # Writes the filename, the relevant keyword, its index number, and its context
                            f.writerow([filename, key, counter, result]) 
                        else:
                            continue

