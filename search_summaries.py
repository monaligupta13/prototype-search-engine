import pickle
import sys
# local module
from text_processing import *

# get top k book summaries for a particluar query
def getSummaries(q, k):
    # pre processing query: tokenization, removing stopwords, stemming
    words = token_list(q)
    if len(words) == 0:
        return []
    else:
        # getting index created for all summaries in database with weight values for a summary and token
        index_file = open("search_data/index.pkl","rb")
        index = pickle.load(index_file)

        # get all matches with score,ids in sorted in desc order of scores
        docScores = get_all_matches(index, words)

        top_matches = []
        # getting summaries data from top summary ids found
        summaries_file = open("search_data/summaries.pkl","rb")
        summaries = pickle.load(summaries_file)
        count = 0
        for el in docScores:
            if count == k:
                break
            top_matches.append(summaries[el[1]])
            count += 1
        index_file.close()
        summaries_file.close()
    return top_matches

def get_all_matches(index, words):
    search_tokens = []
    # getting all summary ids (from index data) containing any of the query tokens
    result = set()
    for word in words:
        if word in index:
            search_tokens += [word]
            entries = [x[0] for x in index[word]]
            result=result|set(entries)

    # scoring for each summary document found
    # adding up wieghts of each token if present in summary document
    docscores = {}
    for query_token in search_tokens:
        for doc_weights in index[query_token]:
            if doc_weights[0] in result:
                if doc_weights[0] in docscores:
                    docscores[doc_weights[0]] += doc_weights[1]
                else:
                    docscores[doc_weights[0]] = doc_weights[1]

    # sorting summary document ids accoring to scores
    docScores=[ [score,doc] for doc,score in docscores.items()]
    docScores.sort(reverse=True)

    return docScores

if __name__ == "__main__":
    print(getSummaries(sys.argv[1], int(sys.argv[2])))
