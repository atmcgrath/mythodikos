# Notes and process Documentation

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
