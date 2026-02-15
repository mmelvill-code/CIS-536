import re
import time
import os
import nltk

class TermFrequencies:
    def __init__(self, doc_freq, global_freq, term=''):
        self.term = term
        self.word_code = 0
        self.doc_freq = doc_freq
        self.global_freq = global_freq

## next tasks

# convert all to ALL CAPS?
# figure out "stemmer" and/or lemmatizer
# store unique stemmed words in a hashtable or dictionary
# write unique stemmed words to dictionary.txt file after reading is complete

wiki_file_path = os.path.join('tiny_wikipedia', 'tinier_wikipedia.txt') # 'tiny_wikipedia.txt')
dictionary_file_path = os.path.join('output', 'dictionary.txt')
unigrams_file_path = os.path.join('output', 'unigrams.txt')

def tokenize_document_to_terms(line):
    terms = re.split(r'\W+', line)
    # RegEx for url: ^https:\/\/[^\s]+ ...

    # perform stemming here?
    # terms = nltk.word_tokenize(line)
    return terms
    
    # # sort the dictionary by global term frequency
    # sorted_by_gf = sorted(full_dict.items(), key=lambda item: item[1].global_freq, reverse=True)

    # with open(unigrams_file_path, "w", encoding="ascii") as dFile :

    #     for k, v in sorted_by_gf:
    #         print(f'{v.word_code} {k} {v.doc_freq} {v.global_freq}', file=dFile)

def process_docs_into_list():

    # dictionary of unique words and associated TermFrequencies. 
    # use this for fast access by term to check presence and assign values to global_freq and doc_freq counters
    d = {}

    l = [] # list of same TermFrequencies for sorting in place

    doc_count = 0
    with open(wiki_file_path, 'r', encoding="ascii") as wiki:
        for doc in wiki:

            doc_terms = set() # empty set, unique words in this article

            terms = tokenize_document_to_terms(doc)

            for term in terms:
                # stemming here or in tokenizer?

                entry = d.get(term) # look for word in dictionary
                if entry is None:
                    # term is not already present in global dictionary
                    newTerm = TermFrequencies(1,1, term) # create new TermFrequencies object
                    d[term] = newTerm # add new word to global list
                    doc_terms.add(term) # add new term to doc terms (can't possibly already be there)
                    l.append(newTerm) # append same new term list for sorting later
                else:
                    term_global_freq = d[term].global_freq
                    d[term].global_freq = term_global_freq + 1
        
                    # has this word already been found in this article?
                    if( term not in doc_terms):
                        # word has not been found in this doc yet
                        term_doc_freq = d[term].doc_freq # get current doc count for this term
                        d[term].doc_freq = term_doc_freq + 1 # increment it
                        doc_terms.add(term) # add it to doc terms list
            doc_count += 1
    print(f'doc_count: {doc_count}')
    return l

def produce_dictionary_file_from_list(list):
    # sort list in-place by term 
    list.sort(key=lambda x: x.term)
    cnt = 0 # this will be word-code
    with open(dictionary_file_path, "w", encoding="ascii") as dFile :
        for item in list:
            print(item.term, file=dFile)
            item.word_code = cnt # set word code for unigrams output
            cnt += 1

def produce_unigrams_file_from_list(list):
    # sort list in-place by global frequency descending
    list.sort(key=lambda x: x.global_freq, reverse=True)

    with open(unigrams_file_path, "w", encoding="ascii") as dFile :
        for item in list:
            print(f'{item.word_code} {item.term} {item.doc_freq} {item.global_freq}', file=dFile)

start_time = time.perf_counter()
global_list = process_docs_into_list()
end_time = time.perf_counter()
print(f"process_docs_into_list() execution time: {end_time - start_time:.4f} seconds")

start_time = time.perf_counter()
produce_dictionary_file_from_list(global_list)
end_time = time.perf_counter()
print(f"produce_dictionary_file_from_list() execution time: {end_time - start_time:.4f} seconds")

start_time = time.perf_counter()
produce_unigrams_file_from_list(global_list)
end_time = time.perf_counter()
print(f"produce_unigrams_file_from_list() execution time: {end_time - start_time:.4f} seconds")
