from handle.mongo import mongo
import json
import re

def get(query):
    db = mongo.get_db()

    print(query)

    query_results = db['contenidos'].find({'Title': {
        "$regex": f'.*{query}.*',
        "$options" :'i' # case-insensitive
        } }, projection={'_id':0})

    list_results = []
    for a in query_results:
        list_results.append(a)

    print(list_results)

    if len(list_results) == 0:
        list_contents = {
            'total': 0,
            'results': None
        }
    else:
        list_contents = {
            'total': len(list_results),
            'results': list_results
        }
    
    return list_contents