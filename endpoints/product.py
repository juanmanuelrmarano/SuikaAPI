from handle.mongo import mongo
import json

def get(product):
    db = mongo.get_db()
    
    cursor = db['contenidos'].find({'Id': product}, projection={'_id':0})
    query_result = list(cursor)

    payload = {
        'PageId': query_result[0]['PageId'],
        'Id'    : query_result[0]['Id'],
        'Title' : query_result[0]['Title'],
        'Link'  : query_result[0]['Link'],
        'Image' : query_result[0]['Image'],
        'Price' : query_result[0]['Price'],
        'Date'  : query_result[0]['Date']
    }

    result = [payload]
    
    if len(result) == 0:
        list_contents = {'results': None}
    else:
        list_contents = {'results': result}
    
    return list_contents