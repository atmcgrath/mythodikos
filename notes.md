# Notes and process Documentation

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
