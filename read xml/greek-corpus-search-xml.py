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
                    cite_list.append(parent.attrs['subtype']+parent.attrs['n']) #printing subtype tells us exactly which parts of the citation are being returned -- comment out later
                except KeyError:
                    continue
            else: continue
        elif 'div' in parent.name:
            try:
                cite_list.append(parent.attrs['type']+parent.attrs['n'])
            except KeyError:
                continue
    cite_list.reverse() # make order book - chapter - section
    citation = '.'.join(cite_list) # make citation format book.chapter.section.line
    return citation
# 4/22 - I cleaned up the citation function (above) It now gets section info for 114 out of 126

def get_linenum(line): # separated functions to test
    textchunk = line.parent # m.parent == the exact section of .xml text in which the match is found (could be a paragraph or a line)
    line_num = ''
    for chunk in textchunk:
        if textchunk.name == 'l' or 'lb': # for line number of match
            try:
                line_num = textchunk.name + textchunk['n']
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

greekcorpusdir = "/Users/amcgrath1/classics/canonical-greekLit-master"
outfile = "/Users/amcgrath1/classics/test-4-22-c.csv"

persondict = {'Atalanta': [r'\bἈταλάντ'],
            'Arion': [r'\bἈρίων', r'\bἈρίον']
            } # Compile in reference to LIMC

placedict = {} # Compile in reference to Barinton Atlas of the Ancient World

# build .csv with desired metadata as column headers
with open(outfile, 'w') as z:
    f = csv.writer(z)
    f.writerow(['person', 'title', 'author', 'section', 'line',
        'match', 'context', 'length', 'filename'])

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
                                section = get_section(m) # applies citation formula to each match
                                line = get_linenum(m)
                                context = m.replace('\n', ' ') # strips newline characters
                                length = len(context) # number of characters in context
                                # context = get_context(m)

                                f.writerow([
                                        key, text_title, text_author, section, line,
                                        t, context, length, file]) #write defined variables for each match to .csv
