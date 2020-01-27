#!/usr/bin/env python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project: building Greek lemma search

Sources:
* cltk: http://docs.cltk.org/en/latest/greek.html#lemmatization
* nltk: https://www.nltk.org/api/nltk.corpus.reader.html?highlight=lemma#nltk.corpus.reader.wordnet.Lemma
	* lemma(name, lang='eng') = return lemma object that matches the name
	* lemma_from_key(key)
	* custom_lemmas(tab_file, lang) = reads custom tab file contianing the mapping of lemmas in the given 
		language to Princeton WordNet 3.0 synset offsets, allowing NLTK WordNet functions to be used with 
		that language
* full form lemma lists in .txt file: https://github.com/stenskjaer/lemmalist-greek
	* possible use: search .txt file for "headword" (i.e. keyword), search .xml corpus for all lemmas, record under keyword

@author: sfritzell
"""

# =====================================================================
# Imports
# =====================================================================


# =====================================================================
# Functions
# =====================================================================


# =====================================================================
# Program
# =====================================================================