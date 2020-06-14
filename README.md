# search-engine-task

BRIEF:

Search built with python-flask

Run create_data.py to create all required data structure from raw data

Search engine functionality:
    Top relevant book summaries for a query
    To test:
        Run search_summaries.py:  python search_summaries.py "query" "K"

Server api "/books":
    GET top relevant books for all queries
    Eg: /books?queries=life&queries=comedians%20details%20spent&K=2

To run server: main.py
