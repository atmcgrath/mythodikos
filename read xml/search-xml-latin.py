#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:56:27 2020

Code for Mythodikos project: Latin search
    1. Open xml, parse xml, find pattern matches for a keyword list
    2. For each match: records line number and line text
    3. Records text section info
    4. Gets title and author of text
    5. Returns one line before and after matching line (as list)
    5. Writes to csv

Next steps:
    1. Check with iteration
    2. Cross reference with placename list
    3. Keyword variations/lemmatized search (Stella)
    4. Create more functions 

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
# Functions
# =============================================================================

def get_citation(line):
    grups = [par.attrs for par in line.parents if par.name == "div"]
    cite_list = []
    for g in grups:
        try:
            cit = g['subtype'] + ' ' + g['n']
            cite_list.append(cit)
        except:
            continue
    cite_list.reverse()
    citation = '; '.join(cite_list)
    return citation
# finds text section information - needs to be tested robustly on corpus

# =============================================================================
# Program
# =============================================================================

infile = "/Users/amcgrath1/Documents/ds-projects/stella-mythodikos/mythodikos/texts/latin-phi0119.xml"

outfile = "/Users/amcgrath1/Documents/ds-projects/stella-mythodikos/mythodikos/data/latin-test-1-24.csv"

with open(outfile, 'w') as z:
    f = csv.writer(z)

    f.writerow(['title', 'author', 'keyword', 'line number', 'section', 'context' 
                #, 'filename'
                ])

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
            citation = get_citation(linematch)
        # line before - previous_sibling is a newline character '\n'

            f.writerow([text_title, text_author, key, linenumber, citation, context])

"""
Notes: could get edition info as part of citation? 
Access highest div parent attribute: n - number subtype = edition?
"""
