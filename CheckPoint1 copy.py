import re
import time
# from collections import namedtuple

class TermFrequencies:
    def __init__(self, doc_freq, global_freq, term=''):
        self.term = term
        self.word_code = 0
        self.doc_freq = doc_freq
        self.global_freq = global_freq

## next tasks

# create function to process a single doc?
# try sorting in place to save memory, don't create two long lists
#   have first sort produce a list of TermFrequencies. 
#   Add 'term' to TermFrequencies members
#   for unigrams, use resulting list of TermFrequences from dictionary.txt, sort it in place

# Convert py file to ipynb.
# convert all to ALL CAPS?

# figure out "stemmer" and/or lemmatizer
# store unique stemmed words in a hashtable or dictionary
# write unique stemmed words to dictionary.txt file after reading is complete

CHUNK_SIZE = 500

def test_01():
    with open('tiny_wikipedia.txt', "r", encoding="ascii") as f1: # open("testfile.txt", "r", encoding="ascii") as f1:

        counter = 0
        max = 4
        last_word = ''
        
        with open('dictionary.txt', "w", encoding="ascii") as dFile :
            
            while(chunk := f1.read(CHUNK_SIZE)):
                counter += 1
                if (counter > max):
                        break
                
                print(chunk)
                print('                            that was the chunk !')

                words = re.split(r'\W+', last_word + chunk)

                last_word = words[len(words) - 1]

                print(words)

                for word in words:
                    dFile.write(word + '\n')
                print('---------------------------------- those were the words! ---------------------------------------')

def tokenize_document_to_terms(line):
    terms = re.split(r'\W+', line)
    # perform stemming here?
    return terms

def process_docs():
    # WordCounts = namedtuple('WordCounts', ['doc_count', 'global_count'], defaults=[0,0])
    d = {} # dictionary of unique words
    doc_count = 0
    with open('tiny_wikipedia.txt', 'r', encoding="ascii") as wiki:
        for doc in wiki:

            doc_terms = set() # empty set, unique words in this article

            terms = tokenize_document_to_terms(doc)

            for term in terms:
                # stemming here or in tokenizer?

                entry = d.get(term) # look for word in dictionary
                if entry is None:
                    newWord = TermFrequencies(1,1) # create new WordFrequencies object
                    d[term] = newWord # add new word to global list
                    doc_terms.add(term) # add new term to doc terms (can't possibly already be there)
                else:
                    # t_cnt = d[term].global_count
                    # d[term]._replace(global_count = t_cnt + 1)
                    term_global_freq = d[term].global_freq
                    d[term].global_freq = term_global_freq + 1
        
                    # has this word already been found in this article?
                    if( term not in doc_terms):
                        # if not, increment doc count for word
                        # d[word].doc_count +=1
                        term_doc_freq = d[term].doc_freq
                        d[term].doc_freq = term_doc_freq + 1
                        doc_terms.add(term)
            doc_count += 1
    print(f'doc_count: {doc_count}')
    return d
    
def produce_output_files(dict):
    
    with open('dictionary.txt', "w", encoding="ascii") as dFile :
        dSorted = sorted(dict)
        for key in dSorted:
            #dFile.write(key  + ' ' + d[key] + '\n')
            #dFile.write('%s %d\n' % (key, d[key]))
            dFile.write(f"{key} {dict[key].doc_freq} {dict[key].global_freq} \n")

        # read dictionary.txt lines
        # identify index of term (line number - 1 in dictionary.txt)
        # lookup frequency of term in dictionary d data structure



def test_sorting():
    wf00 = TermFrequencies(0, 500)
    wf55 = TermFrequencies(5, 900)
    wf99 = TermFrequencies(9, 100)
    orig_dict = {'c': wf00, 'b': wf55, 'a': wf99}


    # make a new list of sorted keys
    sorted_keys = sorted(orig_dict.keys())

    # loop through entire original dictionary setting the word-code
    i=0
    for sk in sorted_keys:
        v = orig_dict[sk]
        v.word_code = i
        i += 1
        print(f'{sk} {v.doc_freq} {v.global_freq}')
    print('----------------------')
    # sort the dictionary by global term frequency
    sorted_items = sorted(orig_dict.items(), key=lambda item: item[1].global_freq, reverse=True)

    for k, v in sorted_items:
        print(f'{k} {v.doc_freq} {v.global_freq}')

def produce_dictionary_file(full_dict):
    # create new list of sorted keys
    sorted_keys = sorted(full_dict.keys())
    cnt = 0
    with open('dictionary.txt', "w", encoding="ascii") as dFile :

        for key in sorted_keys:
            print(key, file=dFile)
            full_dict[key].word_code = cnt
            cnt += 1

def produce_unigrams_file(full_dict):
    
    # sort the dictionary by global term frequency
    sorted_by_gf = sorted(full_dict.items(), key=lambda item: item[1].global_freq, reverse=True)

    with open('unigrams.txt', "w", encoding="ascii") as dFile :

        for k, v in sorted_by_gf:
            print(f'{v.word_code} {k} {v.doc_freq} {v.global_freq}', file=dFile)

def process_docs_into_list():
    # WordCounts = namedtuple('WordCounts', ['doc_count', 'global_count'], defaults=[0,0])
    d = {} # dictionary of unique words and associated WordFrequencies
    l = [] # list of WordFrequencies for sorting in place

    doc_count = 0
    with open('tiny_wikipedia.txt', 'r', encoding="ascii") as wiki:
        for doc in wiki:

            doc_terms = set() # empty set, unique words in this article

            terms = tokenize_document_to_terms(doc)

            for term in terms:
                # stemming here or in tokenizer?

                entry = d.get(term) # look for word in dictionary
                if entry is None:
                    newTerm = TermFrequencies(1,1, term) # create new WordFrequencies object
                    d[term] = newTerm # add new word to global list
                    doc_terms.add(term) # add new term to doc terms (can't possibly already be there)
                    l.append(newTerm)
                else:
                    # t_cnt = d[term].global_count
                    # d[term]._replace(global_count = t_cnt + 1)
                    term_global_freq = d[term].global_freq
                    d[term].global_freq = term_global_freq + 1
        
                    # has this word already been found in this article?
                    if( term not in doc_terms):
                        # if not, increment doc count for word
                        # d[word].doc_count +=1
                        term_doc_freq = d[term].doc_freq
                        d[term].doc_freq = term_doc_freq + 1
                        doc_terms.add(term)
            doc_count += 1
    print(f'doc_count: {doc_count}')
    return l

def produce_dictionary_file_from_list(list):
    # create new list of sorted keys
    list.sort(key=lambda x: x.term)
    cnt = 0
    with open('dictionary2.txt', "w", encoding="ascii") as dFile :

        for item in list:
            print(item.term, file=dFile)
            item.word_code = cnt
            cnt += 1

def produce_unigrams_file_from_list(list):
    
    # sort the dictionary by global term frequency
    list.sort(key=lambda x: x.global_freq, reverse=True)

    with open('unigrams2.txt', "w", encoding="ascii") as dFile :

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

start_time = time.perf_counter()
global_dictionary = process_docs()
end_time = time.perf_counter()
print(f"process_docs() execution time: {end_time - start_time:.4f} seconds")

start_time = time.perf_counter()
produce_dictionary_file(global_dictionary)
end_time = time.perf_counter()
print(f"produce_dictionary_file() execution time: {end_time - start_time:.4f} seconds")

start_time = time.perf_counter()
produce_unigrams_file(global_dictionary)
end_time = time.perf_counter()
print(f"produce_unigrams_file() execution time: {end_time - start_time:.4f} seconds")

# produce_output_files(global_dictionary)
# test_sorting()