# run this to create indexes for words used in book summaries
# to be used in search later
import json
import pickle
import math
# local module
from text_processing import *

# main method
def get_data_store_index():
    # raw summaries data
    summaries_file = open('raw_data/data.json', 'r')
    summaries = json.load(summaries_file)
    index_store = {}
    if "summaries" in summaries:
        # modify into dictionary to use later for search
        modify_summaries(summaries["summaries"])
        # creating index store for all data
        index_store = create_dictionary_data(summaries["summaries"])
    # storing final index to file for later use in search
    index_file = open('search_data/index.pkl', 'wb')
    pickle.dump(index_store, index_file)
    index_file.close()
    summaries_file.close()

# document frequency(df) and inverse document frequency(idf) used to assign a weight to each token for each summary
def create_dictionary_data(summaries):
    total_count = len(summaries)
    # complete index comprising all books to be used for search
    # final format: {token:[[summary_id, weight],[summary_id1, weight1]], token1:....}
    index_store = {}

    for s in summaries:
        # processing index for each summary
        id = s["id"]
        summary = s["summary"]

        # get processed summary text - tokens, removed stopwords and stemming
        tokens = token_list(summary[29:]) # skipping first 29 characters (The Book in Three Sentences: )
        n = len(tokens)
        if n > 0:
            # index for individual summary
            # final format: {token:[summary_id, df], token:...}
            summary_index = document_token_count(n, tokens, id)
            # getting from df from count and n
            summary_index = document_token_df(summary_index, n)
            # for each token in summary
            # adding to final index
            for token, doc_count in summary_index.items():
                if token in index_store:
                    index_store[token].append(doc_count)
                else:
                    index_store[token] = [doc_count]

    # replacing each df for a token and summary with df * idf weight
    index_store = modify_index_with_idf(index_store, total_count)
    return index_store

# token count for each document
def document_token_count(n, tokens, id):
    i = 0
    # index for a particular summary id
    # final format: {token:[summary_id, df], token:...}
    summary_index = dict()
    # counting number of occurances of each token in summary
    for i in range(n):
        if tokens[i] in summary_index:
            summary_index[tokens[i]][1] += 1
        else:
            summary_index[tokens[i]] = [id, 1]
    return summary_index

# replacing each count for a token and summary with df
def document_token_df(summary_index, n):
    # replacing count by document frequency (no of occurances of token in summary / total number of tokens in summary)
    for token, doc_count in summary_index.items():
        doc_count[1] = "%.4f" % (doc_count[1] / n)
        summary_index[token] = doc_count
    return summary_index;

# replacing each df for a token and summary with df * idf weight
def modify_index_with_idf(index_store, total_count):
    # idf: log10(number of summaries / count of summaries in which token occurs)
    for token, allentries in index_store.items():
        n = len(allentries)
        idf = "%.4f" % math.log10(1+(total_count/n))
        for i in range(n):
            # replacing each df for a token and summary with df * idf weight
            index_store[token][i][1] = "%.4f" % (float(index_store[token][i][1]) * float(idf))
    return index_store

# modify summaries json as dictionary to query during search
def modify_summaries(summaries):
    main_dict = dict()
    for s in summaries:
        main_dict[s["id"]] = s
    main_data_file = open('search_data/summaries.pkl', 'wb')
    pickle.dump(main_dict, main_data_file)
    main_data_file.close()

if __name__ == "__main__":
    get_data_store_index()
