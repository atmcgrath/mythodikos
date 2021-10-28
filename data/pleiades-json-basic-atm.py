import json

f = open ('pleiades-places-latest.json')

data = json.load(f)

"""
for i in data:
    print(i)
    @graph 

for i in data["@graph"]:
    id = i["id"]
    title = i["title"]
    print(id)
    print(title)
 @type

"""

def select_type(types):
    place_types = ['villa', 'mountain', 'temple-2']
    relevant = False
    for item in place_types:
        if item in types:
            relevant = True
            break
        else:
            continue
    return relevant


for i in data["@graph"]:
    id = i["id"]
    title = i["title"]
    typ = i["placeTypes"]
    coordinates = i["reprPoint"]
    names = i["names"]
    romanized = names["romanized"]
    if select_type(typ) == True:
        #print(id)
        print(typ)
        print(title)
        #print(coordinates)
        print(romanized)