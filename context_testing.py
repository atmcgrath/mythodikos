#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project:
1. iterates through corpus
2. opens file, parses file, finds pattern matches with regex values & keys in a dictionary
3. locates secondary pattern matches with regex values within initial search results
4. for each match: records latinized person name (key), place name, title & author of text (needs some refinement), citation (with issues), text context (with issues), and file name
5. writes information to .csv

Next Steps:
1. refine 'context' criteria
2. clean up citation extraction, author and title
3. clean up pair-match encoding - should not need to do another find_all() search of the full corpus, just of the initial results
4. attach Pleiades IDs/geo corrdinates to places in search results

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

# greekcorpusdir = "/Users/stellafritzell/mythodikos/canonical-greekLit-master"
# outfile = "/Users/stellafritzell/mythodikos/corpus-test-6-11.csv"

greekcorpusdir = "/Users/amcgrath1/classics/canonical-greekLit-master"
outfile = "/Users/amcgrath1/classics/context-testing-6-11-3.csv"

persondict = {
            'Atalanta': [r'\bἈταλάντ'],
            'Arion': [r'\bἈρίων', r'\bἈρίον']
            } # Compile in reference to https://www.theoi.com/greek-mythology/heroes.html ; eventually LIMC

placedict = {
            'Arcadia': [r'\bἈρκαδ', r'\bἈρκάδ'], #need for lowercase reg-ex as well?
            'Boeotia': [r'\bΒοιωτ', r'\bΒοιῳτ', r'\bΒοϊωτ', r'\bΒοέκ', r'\bβοεκ'],
            #'Calydon': [r'\bΚαλυδόν', r'\bΚαλύδων', r'\bΚαλυδῶν', r'\bΚαλυδών'],
            #'Colchis': [r'\bΚόλκ', r'\bΚολκ', r'\bΚολχ'],
            #'Corinth': [r'\bΚόρινθ', r'\bΚορίνθ', r'\bΚορινθ'],
            #'Lacedaemon': [r'\bΛακεδ', r'\bΛαβεδ', r'\bΛακκοδ', r'\bΛακηδ', r'\bΛακιδ', r'\bΛακοδ', r'\bΛαχεδ'],
            #'Lesbos': [r'\bΛέσβε', r'\bΛέσβη', r'\bΛέσβο', r'\bΛέσβῳ', r'\bΛέσβω'],
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
    f.writerow(['person', #'place',
                'title', 'author', 'section', 'line', 'context', 'length', 'filename'])

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
                        per_terms = persondict[person] # value list for each person key
                        for per in per_terms: # each regex value
                            per_matches = soup.find_all(string=re.compile(per))
                            for per_match in per_matches:
                                rent = per_match.parent 
                                if rent.name == 'l':
                                    try:
                                        sib1 = rent.previous_sibling.previous_sibling.string
                                        sib2 = rent.next_sibling.next_sibling.string
                                        context_big = sib1 + ' ' + per_match + ' ' + sib2
                                    except:
                                        context_big = per_match
                                else:
                                    context_big = per_match.replace('\n', ' ')
                                sentences = re.split("[.;·]", context_big)
                                for sentence in sentences:
                                    con_match = re.search(per, sentence)
                                    if con_match:
                                        context = sentence
                                
                                try:
                                    length = len(context) #number of characters
                                    section = get_section(per_match)
                                    line = get_linenum(per_match)
                                    f.writerow([person, text_title, text_author, section, line, context, length, file])
                                except KeyError:
                                    continue

"""
                                for place in placedict:
                                    pl_terms = placedict[place] # value list for each place key
                                    for pl in pl_terms: # earch regex value
                                        pair = re.search(pl, context) # searches context for x
                                        if pair:
                                            try:
                                                length = len(context) # number of characters
                                                section = get_section(per_match)
                                                line = get_linenum(per_match)
                                                f.writerow([person, place, text_title, text_author, section, line, context, length, file]) # write defined variables for matches to csv
                                            except KeyError:
                                                continue
                                        else:
                                            continue
"""
