#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

'''
Code to clean Pleiades data file for use in the Mythodikos project
1. Opens Pleiades json file
2. Iterates through file data
3. Records desired data for each entry with of a particular place type
4. Fixed issue with reducplication in original code (#out) by adding function -- why did this fix?

Next Steps:
1. Cross reference with Greek corpus search terms
2. Cross reference with Greek corpus search results
3. Expand place types, possibly to include: 'river', 'plain', 'pass', 'resevoir', 'cave', 'cape', 'hill', 'forest', 'mountain', 'island', 'water-open', 'province', 'lake', ...

@author: sfritzell
''' 

# =====================================================================
# Imports & Modules
# =====================================================================
import json

# =====================================================================
# Functions
# =====================================================================
def select_type(types): #to look at Pleiades items only of the specified types
	place_types = ['settlement', 'region']
	relevant = False
	for item in place_types:
		if item in types:
			relevant = True
			break
		else:
			continue
	return relevant

def get_names(name_info): #to get a list of alternate names for desired items
	romanized = []
	for n in name_info:
		item = n['romanized']
		romanized.append(item)
	return romanized


# =====================================================================
# Program
# =====================================================================

infile = "/Users/stellafritzell/mythodikos/pleiades-places-latest.json"
# web url: http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz

outfile = "/Users/stellafritzell/mythodikos/clean-pleiades.json"

with open(outfile, 'w') as z:
	with open(infile) as x:
		data = json.load(x) #parses json file to python dictionary

		# print(data) #prints entire json file

		'''
		for d in data:
			print(d) #print top level keys
		'''
		'''
		for d in data["@graph"]:
			print(d['placeTypes']) #print all placeType entries
		'''

		for d in data["@graph"]:
			typ = d['placeTypes'] #type of place represented by entry
			name = d['title'] #common use (?) name of place
			pl_id = d['id'] #pleiades id number
			gps = d['reprPoint'] #representative lat-long coordinates
			alt_names = d['names'] #returns EVERYTHING under 'names', mostly non-essential

			if select_type(typ) == True:
				name_list = get_names(alt_names)
				data = {name: {'location type': typ, 'Pleiades id': pl_id, 'coordinates': gps, 'other names': name_list}}

				json.dump(data, z, indent=4) #print results in redable format to json outfile


