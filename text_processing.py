from nltk.stem import PorterStemmer
import re

# input: string text
def token_list(text):
    # lowercase to match uppercase letters as well, find stopwords stored in lowercase
    text = text.lower()
    # remove non alphanumeric characters to avoid in indexing
    text = re.sub(r'[^a-z0-9 ]',' ', text)
    # tokenize
    words = text.split()
    stopwords = get_stopwords()
    words = [word for word in words if word not in stopwords]
    # stemming for more matches
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]
    return words

def get_stopwords():
    stopwords_file = open('raw_data/stopwords.txt', 'r')
    stopwords = [stopword.rstrip() for stopword in stopwords_file]
    stopwords_file.close()
    return stopwords
