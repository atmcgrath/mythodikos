#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""

PSEUDOCODE:

1. open infile x
2. identify all proper nouns using NER, return list of strings/tuples x
3. lemmatize all proper noun strings in NER list using CLTK lemmatizer (backoff method), returns list of tuples with lemma & headword
4. if headword in list (index 1 of each tuple) = person from personlist:
	then print to csv (title, author, person, citation, context)
	*** This will be tricky - how to tell code to go back to .xml tags / content for metadata?
5. else:
		continue


CODE for Mythodikos Project: building Greek lemma search

1. opens xml file and pulls all body-type text
2. applies NER to text content, returns a list of tuples representing each line of text
3. lemmatizes a string, returns a list of tuples representing ('lemma', 'headword')

Next Steps:
1. 
2. combine NER and lemmatizing operation to lemmatize ONLY the NER entities
3. determine how to mataintain access to xml metadata
4. Refine NER to catch entities missed on first pass


SOURCES:
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
# Imports & Modules 
# =====================================================================

# modules to read .xml files
import re
from bs4 import BeautifulSoup
# import os # to iterate through files in the corpus

# NLP modules for lemmatizing 
# import nltk
# nltk.download()
# from nltk import word_tokenize
# from nltk import sent_tokenize
# from nltk import WordNetLemmatizer
# from nltk import wordnet
# nltk_lemmas = nltk.WordNetLemmatizer

import cltk
# from cltk.corpus.utils.importer import CorpusImporter
# corpus_importer = CorpusImporter('greek')
# corpus_importer.import_corpus('greek_proper_names_cltk')
# corpus_importer.import_corpus('greek_models_cltk')
# corpus_importer.import_corpus('greek_treebank_perseus')
from cltk.tag import ner
# from cltk.stem.lemma import LemmaReplacer
from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer 
# lemma_build = LemmaReplacer('greek')
lemmatizer = BackoffGreekLemmatizer() # this method returns a list of tuples (lemma, headword)


# =====================================================================
# Functions
# =====================================================================



# =====================================================================
# Program
# =====================================================================

infile = "/Users/stellafritzell/mythodikos/canonical-greekLit-master/data/tlg0001/tlg001/tlg0001.tlg001.perseus-grc2.xml"

soup = BeautifulSoup(open(infile), features="lxml")

personlist = ['Ἀμφιδάμας', 'Μελέαγρος', 'Ζήτης']

# pull the contents of each 'l' tag in the .xml file and ignore other text (i.e. 'title', 'author')
file_text = soup.find_all('l')
for t in file_text:
	text = t.get_text()

	# Apply NER to text (comment out if testing other elements, takes time)
	ner_crawl = ner.tag_ner('greek', input_text=text, output_type=list) # this action returns a string of tuples for each line of text *** FAILS TO IDENTIFY ALL ENTITIES
	# NEXT: merege ALL of the lists OR create loop to iterate through each list at a time -- tuples need to remain distinct
	print(ner_crawl)

"""
	for e in entities: 
		if 'Entity' in e == True:
			print(e)
		else:
			continue
"""

# Testing CLTK lemmatizer
tokens = 'τοῖσιν δʼ Ἀμφιδάμας μυθήσατο, παῖς Ἀλεοῖο·'.split() # reads sentence as a list of strings

print(lemmatizer.lemmatize(tokens)) # this action returns a list of tuples -- returns "μυθήσατο" and "Ἀλεοῖο" incorrectly

