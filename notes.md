# Notes and process Documentation

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
-

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
