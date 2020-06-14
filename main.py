from flask import Flask, request
from find_books import *
app = Flask(__name__)

# API to find books
# inputs: list of queries and integer K to return top K relevant books for each query
@app.route("/books", methods=['GET'])
def books():
    queries = request.args.getlist('queries')
    K = request.args.get('K')

    # Validations for inputs
    if queries:
        if K and K.isdigit():
            K = int(K)

            # get_books from find_books.py
            return get_books(K, queries)
        else:
            return "Invalid K value"
    return "No queries found"

if __name__ == "__main__":
    app.run(debug=True)
