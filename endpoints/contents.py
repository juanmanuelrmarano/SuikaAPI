from handle.mongo import mongo
import json

def get(pageNum):
    db = mongo.get_db()
    
    pageNum = int(pageNum)

    pipeline = [
        {
        "$project" : { 
                "_id": 0,
            }
        },
        { "$skip" : pageNum*9 }, 
        { "$limit" : 9.0 }
    ]

    cursor = db['contenidos'].aggregate(pipeline, allowDiskUse=True)
    list_results = list(cursor)

    count = db['contenidos'].count_documents({})

    print(list_results)

    if len(list_results) == 0:
        list_contents = {'results': None}
    else:
        list_contents = {
            'total': count,
            'results': list_results
        }
    
    return list_contents