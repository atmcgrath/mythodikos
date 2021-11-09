#!/usr/bin/venv python 3
# -*- coding: utf-8 -*-

'''
Code to clean Pleiades data file for use in the Mythodikos project
1. Opens Pleiades json file
2. Iterates through file data
3. Records desired data for each entry with of a particular place type

Next Steps:
1. Address possible reduplication of some results - are these repeat entries in the original file? Is it an issue with the search?
2. Cross reference with Greek corpus search terms
3. Cross reference with Greek corpus search results
4. Expand place types, possibly to include: 'river', 'plain', 'pass', 'resevoir', 'cave', 'cape', 'hill', 'forest', 'mountain', 'island', 'water-open', 'province', 'lake', ...
5. Write function for expanded place types (if 1st item in list, return TRUE, elif 2nd item, ect.)

@author: sfritzell
''' 

# =====================================================================
# Imports & Modules
# =====================================================================
import json

# =====================================================================
# Functions
# =====================================================================
def select_type(types):
	place_types = ['settlement', 'region']
	relevant = False
	for item in place_types:
		if item in types:
			relevant = True
			break
		else:
			continue
	return relevant

# =====================================================================
# Program
# =====================================================================

infile = "/Users/stellafritzell/mythodikos/pleiades-places-latest.json"
# web url: http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz

outfile = "/Users/stellafritzell/mythodikos/clean-pleiades-wfunc.json"

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
			name = d['title'] #common use (?) name of place
			pl_id = d['id'] #pleiades id number
			gps = d['reprPoint'] #representative lat-long coordinates
			#alt_names = d['names'] #this doesn't seem like useful information right now (it has a lot of extra stuff)
			typ = d['placeTypes'] #type of place represented by entry
			'''
			if "settlement" in typ:
				ptyp = "settlement"
				data = {name: {'location type': typ, 'Pleiades id': pl_id, 'coordinates': gps, 'place type': ptyp}}
			elif "region" in typ:
				ptyp = "region"
				data = {name: {'location type': typ, 'Pleiades id': pl_id, 'coordinates': gps, 'place type': ptyp}}
			'''
			if select_type(typ) == True:
				data = {name: {'location type': typ, 'Pleiades id': pl_id, 'coordinates': gps}}

				json.dump(data, z, indent=4) #print results in redable format to json outfile


