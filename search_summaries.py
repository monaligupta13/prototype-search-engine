import pickle
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
