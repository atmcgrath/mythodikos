# Notes and process Documentation

## June 24 Meeting

- Stella fixed the problems with the context search and is testing it out as a function.

Questions about getting data from multiple csv files and/or reading and writing to csv
- Open pleaides file, read it, search for a match between place and place, take lat/long and add to a column
- Open 2 csvs and make a 3rd from the data

```python
# This is very, very rough, untested, and sketchy
with open(infile1, 'r') as z #open match results
  f = csv.reader(z)

  match_data = []
  places = []
  for row in f
    match_data.append(row) # creates a list from data - list(csv.reader) can only be iterated once
    placename = row[10]
    places.append(placename)
    sets = set(places) # removes duplicates from the place list

geo_data = {}
pleaides = list(csv.reader(infile2)) # creates a list from the data
  location = row[8]
  if location in sets:
    geo_data[location] = row[3], row[7]

# data header thing

for row in read_results # list from csv of person & place matches
  if row[8] in pleaides:


```

### Immediate priorities
- Test the function
- Reading the csv file

## June 12 Meeting

- Looking at previous code for getting context: it isn't splitting on the punctuation
- My suggestions - try:
  - Getting rid of try/except (see error source)
  - Using regex syntax
- I ran the code - did not even get variables for sib1 and sib2 which means the problem is with the 'if' statement
- fixed: .name instead of .t
- added spaces between

```python

sib1 = per_match.parent.previous_sibling.previous_sibling.string

```
Ran it again and it seems to have worked, barring 2 exceptions (first line and last line?)

```python
try:
    sib1 = per_match.parent.previous_sibling.previous_sibling.string
    sib2 = per_match.parent.next_sibling.next_sibling.string
    siblings = sib1 + ' ' + per_match + ' ' + sib2 #string with lines before and after
    sentences = re.split("[.;•]", siblings )
    for sentence in sentences:
        con_match = re.search(per, sentence)
        if con_match:
            context = sentence
except:
      context = "CONTEXT ERROR"
```
- Replaced dot (copied and pasted) in the middle of a line: Stella will see if this worked

- Implemented sentence-splitting all context matches, not just lines:

```python
rent = per_match.parent
if rent.name == 'l'
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

```

This definitely reduces the length of the context segments, but I can't tell if they are split as they should be, so let me know! See output: /data/context-testing-6-11-3.csv


### Next steps:
- [ ] Fix first/last line errors (missing siblings) - currently handles exception by limiting to the single line: find way to include any existing siblings.
- [ ] Make it into a function?

<!--
Good workflow - commit each time I change Stella's code, then
-->


## May 27 meeting

- Updated timeframe for Summer: extracting sample dataset & creating proof-of-concept map.
- Place names
  - Pleaides for geocoding
  - Python to read CSV data: https://docs.python.org/3/library/csv.html
  - Adding to list of place names at the moment
- Help with: context and line numbers

### Context

Restrict the context to sentences, divided by major punctuation marks
- Create a regex object that includes all needed punctuation []
- Join siblings and match to single string
- re.split on regex to create list of sentences
- Iterate through to locate match instance

Alice sample code (untested)

```python
  sib1 = per_match.previous_sibling.string
  sib2 = per_match.next_sibling.string
  siblings = sib1+per_match+sib2 # string with lines before and after
  sentences = siblings.re.split(regex) # returns list of sentences
  for sentence in sentences:
    match = re.search(per, sentence)
    if match:
      context = sentence
```
### Line numbers

Refining line number functions:
- What it looks like: <lb n="175"/> tlg0533 17
- Why it doesn't work: because lb doesn't contain any text.

How to get this line number:
- It's still a child of <p>
- It doesn't technically 'contain' the text
- per_match.parent.lb

Does the line number thing work often?
- Worked for: tlg2046.tlg001.perseus-grc1.xml (has <l>text</l>)
- Works for latin example, but there are so few matches overall

## Feb 14, 2020 Meeting - ATM notes
- I changed "infile" to "file" so it writes just filename instead of entire filepath (99)
- Also added a column for m to see what's going on here (99)
- It was stopping after 65 matches because there was a text part with no number. I fixed that by adding a try/except to the function (41-46):

```python
    for s in sections: # for each 'div' attributes dictionary
        if s['type'] == 'textpart' or 'chapter':
            try:
                cite_list.append(s['n'])
            except:
                continue
        else:
            continue

```
- Then it stopped at 85 because there was a text without an author. I fixed that (81-82):

```python

if soup.author:
  text_author = soup.author.string
else: text_author = ""

```
If you look at my branch you can see the whole code, but I had to fix the indenting also so it doesn't give you a granular changelog.


## Jan 31, 2020 Meeting - ATM notes

Discussed [lemma_search.py](lemma_search.py)
- NER and Lemmatizer
- Getting better output (list of tuples featuring entities)

Action items Alice
- [ ] Use lemmatizer to filter NER list or vice versa
- [ ] OR just sort greek NER list?
- [ ] Work on adding place name search to [latin xml search](search-xml-latin.py)
- [ ] More testing of get_citation() - see comments in search-xml-greek.py

Thoughts:
- Do we need to NER every time? Text search might be easier
- Maybe we just do it once to narrow down a list of places?
- NER and Lemmatizer take forever - how can we optimize speed?


Output as dictionary:
1. Iterate through lines;
2. For each line return line number and entities present
3. Create a dictionary of lines that have entities
4. Filter dictionary for relevant headwords (personal names) using lemmatizer

Testing this github.dev thing