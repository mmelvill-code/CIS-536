import re
import time
import os
import nltk
nltk.data.path.append('./nltk_data')
# from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as wnl

class TermFrequencies:
    def __init__(self, doc_freq, global_freq, term=''):
        self.term = term
        self.word_code = 0
        self.doc_freq = doc_freq
        self.global_freq = global_freq

## next tasks

# check notes for other requirements mentioned
    # throw out stop words?
# check accuracy of readme.txt before submit

# submit: 
    # CheckPoint1.py
    # readme.txt
    # dictionary.txt
    # unigrams.txt

wiki_file_path = 'tiny_wikipedia.txt' # 'tiny_wikipedia.txt' #'tinier_wikipedia.txt'
dictionary_file_path = 'dictionary.txt'
unigrams_file_path = 'unigrams.txt'

splitter = r'[^a-zA-Z0-9_-]'

def tokenize_document_to_terms(line):

    # remove https://en.wikipedia.org/wiki?curid=########## and all other urls
    # line = re.sub(r'^[^ ]* ', '', line)
    line = re.sub(r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)', '', line)

    # remove #lt;---these-tags-and-the-stuff-between-them---#gt;
    line = re.sub(r'#[a-z]+;[a-zA-Z_-]+#[a-z]+;', '', line)

    # replace #amp; and similar with space 
    line = re.sub('#[a-z]+;', ' ', line)

    # split by all non alphanumeric values, allow underscore (_) and dash (-)
    terms = re.split(splitter, line)

    return terms

def lemmatize_token(token):
    # stemming here 
    # if starts or ends with dashes or underscores, remove dashes and underscores
    token = re.sub(r'((^[-_]+(?=[a-zA-Z0-9_-]))|((?<=[a-zA-Z0-9_-])[-_]+$)|^([-_]+)$)', '', token)

    # convert to all lower case
    token = token.lower()

    return wnl().lemmatize(token)

def process_docs_into_list():

    # dictionary of unique words and associated TermFrequencies. 
    # use this for fast access by term to check presence and assign values to global_freq and doc_freq counters
    d = {}

    l = [] # list of same TermFrequency objects for sorting in place

    doc_count = 0
    with open(wiki_file_path, 'r', encoding="ascii") as wiki:
        for doc in wiki:

            doc_tokens = set() # empty set, unique words in this article

            tokens = tokenize_document_to_terms(doc)

            for token in tokens:
                # stemming here 
                term = lemmatize_token(token)
                if(term==''):
                    continue

                entry = d.get(term) # look for word in dictionary
                if entry is None:
                    # term is not already present in global dictionary
                    newTerm = TermFrequencies(1,1, term) # create new TermFrequencies object
                    d[term] = newTerm # add new word to global list
                    doc_tokens.add(term) # add new term to doc terms (can't possibly already be there)
                    l.append(newTerm) # append same new term list for sorting later
                else:
                    term_global_freq = d[term].global_freq
                    d[term].global_freq = term_global_freq + 1
        
                    # has this word already been found in this article?
                    if( term not in doc_tokens):
                        # word has not been found in this doc yet
                        term_doc_freq = d[term].doc_freq # get current doc count for this term
                        d[term].doc_freq = term_doc_freq + 1 # increment it
                        doc_tokens.add(term) # add it to doc terms list
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
