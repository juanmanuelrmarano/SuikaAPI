from handle.mongo import mongo
import json

def get(history):
    db = mongo.get_db()
    
    cursor = db['scraping'].find({'Id': history}, projection={'_id':0})
    # cursor = db['historial'].find({'Id': history}, projection={'_id':0})
    query_result = list(cursor)

    print('QUERY', query_result, "\n\n" )

    payload = {
        'PageId': query_result[0]['PageId'],
        'Id'    : query_result[0]['Id'],
        # 'Title' : query_result[0]['Title'],
        # 'Link'  : query_result[0]['Link'],
        # 'Image' : query_result[0]['Image'],
        'Price' : query_result[0]['Price'],
        'Date'  : query_result[0]['Date']
    }

    print('PAYLOAD', payload, "\n\n" )

    result = [payload]
    
    if len(result) == 0:
        list_contents = {'results': None}
    else:
        list_contents = {'results': result}
    
    return list_contents