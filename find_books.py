from multiprocessing import Process, Queue
from flask import jsonify
import requests
# local module
from search_summaries import *

# books queue to maintain while multiprocessing queries
books_queue = Queue()

# main method to get books for all queries
def get_books(k, queries):
    processes = []
    # multiprocessing queries: search engine used for each query simultaneously
    # queryBooks method to get books for a single query
    for q in queries:
        processes += [Process(target=queryBooks, args=(q, k))]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    books_arr = []
    while not books_queue.empty():
        books_arr += [books_queue.get()]
    return jsonify(books_arr)

# process book search for a single query
def queryBooks(q, k):
    # using search engine built for a single query,K pair
    search_result = getSummaries(q, k)

    # getting authors for each book
    if search_result != []:
        for index, book in enumerate(search_result):
            author_res = requests.post('https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding', json={'book_id': book["id"]})
            search_result[index]['query'] = q
            search_result[index]['author'] = author_res.json()["author"]
        # adding each query result to the main queue
        books_queue.put(search_result)
