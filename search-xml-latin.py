#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:56:27 2020

Code for Mythodikos project: Latin search
    1. Open xml, parse xml, find pattern matches
    2. For each match: records line number and line text
    3. Returns three lines around keyword match

Next steps:
    1. Write to csv
    2. Keyword list
    3. Keyword variations/lemmatized search
    4. Clean up

@author: amcgrath1
Based on search-xml-greek.py
"""

# =============================================================================
#  Imports
# =============================================================================

from bs4 import BeautifulSoup
import re
import csv

# =============================================================================
# Program
# =============================================================================

infile = "/Users/amcgrath1/Documents/ds-projects/stella-mythodikos/mythodikos/texts/latin-phi0119.xml"

outfile = "/Users/amcgrath1/classics/mytho-test-1-24.csv"

with open(outfile, 'w') as z:
    f = csv.writer(z)

#f = csv.writer(open(outfile, 'w'))
    f.writerow(['title', 'author', 'keyword', 'line', 'context', 'filename'])

    keywords = ['argumentum', 'faciundum', 'antiquam']

    soup = BeautifulSoup(open(infile), features="lxml")

    text_title = soup.title.string
    text_author = soup.author.string

    for key in keywords:
        matches = soup.find_all(string=re.compile(key))
    
# creates list of string matches 
        for m in matches: # m represents matching string
            linematch = m.parent # linematch represents line containing m
            linenumber = m.parent['n'] # line number attribute of linematch
            prev_line = linematch.previous_sibling.previous_sibling.string
            next_line = linematch.next_sibling.next_sibling.string
            context = [prev_line, m, next_line]
        # line before - previous_sibling is a newline character '\n'

            f.writerow([text_title, text_author, key, linenumber, context, infile])


