#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

"""
Code for Mythodikos Project:
1. iterates through corpus
2. opens file, parses file, finds pattern matches with regex values & keys in a dictionary
3. locates secondary pattern matches with regex values within initial search results
4. for each match: records latinized person name (key), place name, title & author of text (needs some refinement), citation (with some issues), text context, context length and file name
5. writes information to .csv (write to .json commented out) (NOTE: .json searches / writes much faster than .csv)

Next Steps:
1. clean up citation extraction, author and title
2. attach Pleiades IDs/geo corrdinates to places in search results (read Pleiades data .json - write to mythodikos data .json) -- use Pandas
3. make persondict and placedict idependent (json?) files that are called by the code -- useful when expanding dataset
4. write to download/access most recent Perseus corpus and Pleiades file

@author: sfritzell
adapted from: search-xml-greek.py
"""

# =====================================================================
# Imports & Modules
# =====================================================================

import os # to search file directory
import fnmatch # to specify files
import re # to use regex functions to search keywords
from bs4 import BeautifulSoup # to read xml files
#import csv # to write search results to csv
import json # to write search results to json

# =====================================================================
# Functions
# =====================================================================

def get_section(line): #function to get the section citation info from xml
	cite_list = [] #creates empty list for citation information
	for parent in line.parents: #for parents of keyword match
		if parent.name == 'div': #if the parent is a div
			if parent.attrs['type'] == 'textpart': #and if the div has textpart as an attibute
				try:
					cite_list.append(parent.attrs['subtype']+parent.attrs['n']) #grab the subtype (book, chapter, section) and the number
				except KeyError: #if this doesn't work for one instance, keep going
					continue
			else: continue #if the div doesn't have this attribute, keep going
		elif 'div' in parent.name: #if the the xml encoding is differnt, div might be in the parent name
			try:
				cite_list.append(parent.attrs['type']+parent.attrs['n']) #in that case, grab the type and number
			except KeyError:
				continue
	cite_list.reverse() #make the citation order: book,chapter,section
	citation = '.'.join(cite_list) #make format: book.chapter.section
	return citation #print the citation

def get_linenum(line): #separated from get_section to test, function to get the line number citation info from xml
	textchunk = line.parent #the exact section of .xml text in which the match is found (could be a paragraph or a line)
	line_num = '' #create an empty variable for the line number
	for chunk in textchunk: #for each element in textchunk
		if textchunk.name == 'l' or 'lb': #if the textchunk is marked as a line
			try:
				line_num = textchunk.name + ' ' + textchunk['n'] #line number is "line"+number
			except KeyError: #if this doesn't work for one instance, keep going
				continue
		else: #if textchunk isn't marked as a line, keep going
			continue
	return line_num #print the line number

def get_context(line): #function to get the text context for search matches from xml
	context = '' #create empty variable for context
	rent = line.parent #the exact section of .xml text in which the match is found
	if rent.name == 'l': #if text uses lines/line numbers, get the immediate, previous, and following lines
		try:
			sib1 = rent.previous_sibling.previous_sibling.string #the line before the match line
			sib2 = rent.next_sibling.next_sibling.string #the line after the match line
			context_big = sib1 + ' ' + line + ' ' + sib2 #string of three lines
		except:
			try:
				context_big = sib1 + ' ' + line #if there's no line following the match line, return a string of two lines
			except:
				try:
					context_big = line + ' ' + sib2 #if there's no line before the match line, return a string of two lines
				except:		
					context_big = line #if there's no lines before or after match line, return the match line
	else: #if the text doesn't use lines/line numbers, get the text chunk of the match
		context_big = line.replace('\n', ' ') #replaces newline characters in the text chunk with space
	sentences = re.split("[.;·]", context_big) #split the context_big text chunks at major punctuation breaks
	for sentence in sentences: #for each string in the text chunk
		con_match = re.search(per, sentence) #if there is a keyword match in the string
		if con_match:
			context = sentence 
	return context #print the sting as match context

# =====================================================================
# Program
# =====================================================================

greekcorpusdir = "/Users/stellafritzell/mythodikos/canonical-greekLit-master" #directory with files for text mining
outfile = "/Users/stellafritzell/mythodikos/corpus-test-10-27.json" #file to write search data, change file type to .json with .json search

#list of 1st keywords
persondict = {
			'Achilles': [r'\bἈχιλλε', r'\bἈχιλλέ', r'\bἈχιλε', r'\bἈχιλέ'], #may be getting some false results, double check regex
			'Actaeon': [r'\bἈκταίων', r'\bἈκταίον'],
			'Adonis': [r'Ἄδωνις', r'Ἄδωνιν', r'\bἈδώνιδ', r'\bἈδωνίδ'], #overlap with festival / month names
			'Amymone': [r'\bἈμυμώνη', r'\bἈμυμώνῃ', r'\bἈμυμώνα', r'\bἈμυμῶνα', r'\bἈμυμόνη'], #also the name of a river
			'Andromeda': [r'\bἈνδρομέδα', r'\bἈνδρομέδᾳ', r'\bἈνδρομέδη', r'\bἈνδρομέδῃ'],
			'Antiope': [r'\bἈντιόπ'],
			'Arachne': [r'\bἈράχνη', r'\bἈράχνῃ'],
			'Arion': [r'\bἈρίων', r'\bἈρίον'], #also the name of a horse
			'Ascalabus': [r'\bἈσκάλαβο'],
			'Asclepius': [r'\bἈσκληπιό', r'\bἈσκληπιο', r'\bἈσκλήπιο', r'Ἀσκληπιέ', r'\bἈσκλαπ'],
			'Atalanta': [r'\bἈταλάντ'],
			'Bellerophon': [r'\bΒελλερεφόντα', r'\bΒελλεροφόντα', r'\bΒελερόφοντα', r'\bΒελλερεφόντη', '\bΒελλερεφόντῃ', r'\bΒελλεροφόντῃ', r'\bΒελλεροφόντη', r'\bΒελεροφόντη', r'\bΒελλεροφόντο', r'\bΒελλερόφοντο', r'\bΒελερόφοντο', r'\bΒελεροφόντο', r'\bΒελλεροφώ', r'\bΒελλεροφῶ'],
			'Busiris': [r'\bΒούσιρι', r'\bΒουσίριδ'],
			'Cadmus': [r'Κάδμε', r'\bΚάδμοι', r'\bΚάδμον', r'\bΚάδμος', r'\bΚάδμου', r'\bΚάδμω', r'\bΚάδμῳ'],
			'Callisto': [r'\bΚαλλιστώ', r'Καλλιστῆς', r'Καλλιστοῖ', r'Καλλιστοῦς'],
			'Cecrops': [r'\bΚέκροψ', r'\bΚέκρωψ', r'\bΚέκροπο', r'\bΚέκροπα', r'\bΚέκροπε', r'\bΚεκρόπε', r'Κέκροπι'],
			'Coronis': [r'Κορωνίς', r'\bΚορωνίδα', r'\bΚορωνίδο', r'\bΚορωνίδι'], #there are multiple Coronises
			'Cycnus': [r'\bΚύκνο', r'\bΚύκνῳ', r'\bΚύκνω', r'Κύκνε'], #there are multiple Cycnuses, typically identified by toponym --> seperation will occur in search/data collection
			'Cyparissus': [r'\bΚυπάρισσο', r'\bΚυπαρίσσο', r'\bΚυπαρισσο', r'\bΚυπάριτ', r'\bΚυπαρίτ'], #also a city name
			'Cyrene': [r'\bΚυρήνη', r'\bΚυρήνῃ', r'\bΚυράνα', r'\bΚυράνᾳ'], #also a city name
			'Danae': [r'\Δανάη', r'\bΔανάῃ', r'\bΔανάα'],
			'Deucalion': [r'\bΔευκαλίω', r'\bΔευκαλλίω'],
			'Diomedes': [r'\bΔιομήδη', r'\bΔιομήδῃ', r'\bΔιομήδο', r'\bΔιομήδε', r'\bΔιόμηδε'], #may be getting some false results, overlap with female name Diomede, adjectival use
			'Endymion': [r'\bἘνδυμίων'],
			'Erysichthon': [r'\bἘρυσίχθ', r'\bἘρισίχθ'],
			'Eryx': [r'Ἔρυξ', r'Ἔρυκα', r'\bἘρύκη', r'\bἘρύκῃ', r'\bἜρυκι', r'\bἜρυκο'], #there are multiple Eryxes, also a city name, TLG finds only a feminine name - contrast with male figure in THEOI
			'Europa': [r'\bΕὐρώπη', r'\bΕὐρώπῃ', r'\bΕὐρώπα', r'\bΕὐρώπᾳ'], #also a place name, may be getting some false results
			'Euadne': [r'\bΕὐάδν'], #there are multiple Euadnes
			#'Ganymede': [r'\b'],
			#'Geryon': [r'\b'],
			#'Heracles': [r'\b'],
			'Hippolyta': [r'\bἹππολύτα', r'\bἹππολύτη'],
			#'Hyacinthus': [r'\b'],
			#'Iamus': [r'\b'],
			#'Iasion': [r'\b'],
			#'Icarius': [r'\b'],
			#'Io': [r'\b'],
			#'Ixion': [r'\b'],
			#'Jason': [r'\b'],
			#'Leda': [r'\b'],
			#'Lycaon': [r'\b'],
			#'Lycurgus': [r'\b'],
			'Meleager': [r'\bΜελέαγρ', r'\bΜελεάγρ'], #may be getting some false results, overlap with festival name
			'Midas': [r'\bΜίδα', r'\bΜίδᾳ', r'\bΜίδη', r'Μίδου', r'Μίδῃ', r'Μίδεω', r'\bΜῖδα'],
			#'Minyades': [r'\b'], #a trio of princesses
			'Narcissus': [r'\bΝάρκισσο', r'\bΝαρκίσσο', r'Ναρκίσσῳ', r'\bΝάρκισο', r'\bΝαρκίσο'],
			#'Odysseus': [r'\b'],
			#'Oedipus': [r'\b'],
			#'Orestes': [r'\b'],
			#'Orion': [r'\b'],
			#'Otrera': [r'\b'],
			#'Pandora': [r'\b'],
			'Pasiphae': [r'\bΠασιφάη', r'\bΠασιφάῃ', r'\bΠασιφάα'],
			'Pelops': [r'\bΠέλο'], #accent should limit results in regex
			#'Penthesilea': [r'\b'],
			#'Perseus': [r'\b'],
			#'Phaethon': [r'\b'],
			#'Psyche': [r'\b'],
			#'Pygmalion': [r'\b'],
			#'Pyrrha': [r'\b'],
			#'Salmoneus': [r'\b'],
			#'Sisyphus': [r'\b'],
			#'Tantalus': [r'\b'],
			#'Tennes': [r'\b'],
			#'Theseus': [r'\b'],
			#'Tithonus': [r'\b'],
			#'Triptolemus': [r'\b'],
			#'Tyro': [r'\b']
			} # Compile in reference to https://www.theoi.com/greek-mythology/heroes.html ; eventually LIMC

#list of 2nd keywords - eventually add lowercase reg-ex for adjectival / toponymical uses
placedict = {
			'Arcadia': [r'\bἈρκαδ', r'\bἈρκάδ'],
			'Boeotia': [r'\bΒοιωτ', r'\bΒοιῳτ', r'\bΒοϊωτ', r'\bΒοέκ', r'\bΒοεκ'],
			'Calydon': [r'\bΚαλυδόν', r'\bΚαλύδων', r'\bΚαλυδῶν', r'\bΚαλυδών'],
			'Colchis': [r'\bΚόλκ', r'\bΚολκ', r'\bΚολχ'],
			'Corinth': [r'\bΚόρινθ', r'\bΚορίνθ', r'\bΚορινθ'],
			'Lacedaemon': [r'\bΛακεδ', r'\bΛαβεδ', r'\bΛακκοδ', r'\bΛακηδ', r'\bΛακιδ', r'\bΛακοδ', r'\bΛαχεδ'],
			'Lesbos': [r'\bΛέσβε', r'\bΛέσβη', r'\bΛέσβο', r'\bΛέσβῳ', r'\bΛέσβω'],
			#'Lycaeus': [r''],
			#'Mainalos': [r''],
			#'Methymna': [r''],
			#'Parthenion': [r''],
			#'Taenarum': [r''],
			#'Tarentum': [r''],
			#'Tegea': [r''],
			'Thebes': [r'\bΘήβ', r'\bΘῆβ']
			} # Compile in reference to filtered Pleiades data, TLG lemma search for varient Greek spellings

#build json (#csv) file with desired search metadata
with open(outfile, 'w') as z: #to access/create the outfile for data from text-mining
	#f = csv.writer(z)
	#f.writerow(['person', 'place', 'title', 'author', 'section', 'line', 'context', 'length', 'filename'])

	for root, dirs, files in os.walk(greekcorpusdir):
		for file in files:
			if fnmatch.fnmatch(file, '*grc*.xml'): #for each file in the directory marked as Greek 
				infile = root+'/'+str(file) #identify these files to be searched
				
				with open(infile) as x: #open and iterate through each identifed file
					soup = BeautifulSoup(x, features='lxml')

					text_title = soup.title.string #create variable for text title
					if soup.author: #if an author is recorded for the file
						text_author = soup.author.string #create a variable for text author
					else: text_author = '' #otherwise record text author as blank

					# could I insert a 'with open(file)' command here to access a seperate person-dict file?
					for person in persondict:
						per_terms = persondict[person] # value list for each person key
						for per in per_terms: # each regex value
							per_matches = soup.find_all(string=re.compile(per)) #using soup.find_all in place of re.search for navigating xml
							for per_match in per_matches:
								context = get_context(per_match)

								# could I insert a 'with open(file)' command here to access a seperate place-dict file?
								for place in placedict:
									pl_terms = placedict[place] # value list for each place key
									for pl in pl_terms: # earch regex value
										pair = re.search(pl, context) # searches context for x
										if pair:
											try:
												section = get_section(per_match)
												line = get_linenum(per_match)
												length = len(context) # number of characters
												#f.writerow([person, place, text_title, text_author, section, line, context, length, file]) # write defined variables for matches to csv
												data = {person + '-' + place: {'person': person, 'place': place, 'citation': [text_author, text_title, section, line], 'text': context, 'length': length, 'file': file}}
												json.dump(data, z, indent=4)
											except KeyError:
												continue
										else:
											continue

# write code to attach geo coordinates to dataset from Pleiades .csv or .json file