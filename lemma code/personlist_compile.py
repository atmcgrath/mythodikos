#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-


"""
This program should: 
1. filter the CLTK lemma dictionary using the CLTK proper-nouns list
2. find variants of selected personnames by seraching the filtered lemma dictionary
3. create a dictionary/list with the slected personnames/headwords as keys and the lemma variants as values: {'headword':[variant1, variant2, variant3], ... }

Shortcomings:
* This will return proper-name variants of proper-names, but not adjectival forms, which will be needed to search for placenames

PSEUDOCODE
1. open CLTK proper-nouns list
2. open CLTK lemma dictionary
3. for key.value in CLTK lemma dictionary:
	if value in CLTK proper-nouns list
		then ....

CODE
1. opens the CLTK proper names text file, removes non-alpha characters, tokenizes the contents (creates a list of strings), sorts contents, removes duplicates
2. opens CLTK lemma dictionary, removes non-alpha characters

NEXT STEPS
1. iterate through lemma dictionary for matches with name list
2. create dictionary with matched lemma values as keys, matched keys as values

"""
# =====================================================================
# Imports & Modules
# =====================================================================

import nltk
from nltk import word_tokenize
import greek_accentuation 
from greek_accentuation.characters import strip_breathing
from greek_accentuation.characters import strip_accents
from greek_accentuation.characters import base

"""
from bs4 import BeautifulSoup
import cltk
import re
"""

# =====================================================================
# Program
# =====================================================================

proper_names = "/Users/stellafritzell/cltk_data/greek/lexicon/greek_proper_names_cltk/proper_names.txt"
lemma_dict = "/Users/stellafritzell/cltk_data/greek/model/greek_models_cltk/lemmata/greek_lemmata_cltk.py"

# ALPHA SORT NAMES
dirty_list = open(proper_names, "r") # opens file
clean_names = strip_accents(strip_breathing(dirty_list.read())) # reads file, removes all diacritic characters 
tokens = word_tokenize(clean_names) # makes each entry a string in a list
tokens.sort() # sorts the name list 
name_list = list(dict.fromkeys(tokens)) # removes duplicates created by removal of accents
del name_list[0 : 17] # removes index 0-16 with "|" character (alpha only duplicates already in list), "for" loop below only removes some of the items

"""
for name in name_list:
	if "|" in name:
		name_list.remove(name)
"""

dirty_lemmas = open(lemma_dict, "r") # opens file
clean_lemmas = strip_accents(strip_breathing(dirty_lemmas.read())) # reads file, removes all non-alpha characters (This is slow!)

# FIND LEMMA-NAME MATCHES
for lemma in clean_lemmas:
	if lemma in name_list:
		print(lemma)

personlist = ['Ἀμφιδάμας', 'Μελέαγρος', 'Ζήτης']



