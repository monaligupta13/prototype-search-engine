# run this to create indexes for words used in book summaries
# to be used in search later

import json
import pickle
import math
# local module
from text_processing import *

# main method
# document frequency(df) and inverse document frequency(idf) used to assign a weight to each token for each summary
def create_dictionary_data():
    # raw summaries data
    summaries_file = open('raw_data/data.json', 'r')
    summaries = json.load(summaries_file)
    if "summaries" in summaries:
        # modify into dictionary to use later for search
        modify_summaries(summaries["summaries"])

        total_count = len(summaries["summaries"])
        # complete index comprising all books to be used for search
        # final format: {token:[[summary_id, weight],[summary_id1, weight1]], token1:....}
        index_store = {}

        for s in summaries["summaries"]:
            # processing index for each summary
            id = s["id"]
            summary = s["summary"]

            # get processed summary text - tokens, removed stopwords and stemming
            tokens = token_list(summary[29:]) # skipping first 29 characters (The Book in Three Sentences: )
            # index for individual summary
            # final format: {token:[summary_id, df], token:...}
            summary_index = dict()
            n = len(tokens)
            if n > 0:
                i = 0
                # counting number of occurances of each token in summary
                for i in range(n):
                    if tokens[i] in summary_index:
                        summary_index[tokens[i]][1] += 1
                    else:
                        summary_index[tokens[i]] = [id, 1]
                # for each token in summary
                # replacing count by document frequency (no of occurances of token in summary / total number of tokens in summary)
                # adding to final index
                for token, doc_count in summary_index.items():
                    summary_index[token][1] = "%.4f" % (summary_index[token][1] / n)
                    if token in index_store:
                        index_store[token].append(doc_count)
                    else:
                        index_store[token] = [doc_count]

        # replacing each df for a token and summary with df * idf weight
        # idf: log10(number of summaries / count of summaries in which token occurs)
        for token, allentries in index_store.items():
            n = len(allentries)
            idf = "%.4f" % math.log10(total_count/n)
            for i in range(n):
                # replacing each df for a token and summary with df * idf weight
                index_store[token][i][1] = "%.4f" % (float(index_store[token][i][1]) * float(idf))

        # storing final index to file for later use in search
        index_file = open("search_data/index.pkl","wb")
        pickle.dump(index_store, index_file)
        index_file.close()

    summaries_file.close()

# modify summaries json as dictionary to query during search
def modify_summaries(summaries):
    main_dict = dict()
    for s in summaries:
        main_dict[s["id"]] = s
    main_data_file = open("search_data/summaries.pkl","wb")
    pickle.dump(main_dict, main_data_file)
    main_data_file.close()

if __name__ == "__main__":
    create_dictionary_data()
