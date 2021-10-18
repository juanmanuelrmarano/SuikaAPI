from handle.mongo import mongo
import json

def get(history):
    db = mongo.get_db()
    
    cursor = db['historial'].find({'Id': history}, projection={'_id':0}).sort('Date')
    query_result = list(cursor)

    print('QUERY', query_result, "\n\n" )
    
    if len(query_result) == 0:
        list_contents = {'results': None}
    else:
        list_contents = {'results': query_result}
    
    return list_contents