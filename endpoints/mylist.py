from handle.mongo import mongo
import json

def get(publicHash):
    db = mongo.get_db()

    print(publicHash)

    cursorMyList = db['usuarios'].find_one({'PublicHash': publicHash})

    if cursorMyList == None:
        list_contents = {'results': None}

    list_results = []
    for item in cursorMyList['MyList']:
        pipeline = [
            {
                "$match" : {
                    "Id" : item
                }
            },
            {"$sort": {'Title': 1} },
            { 
                "$project" : { 
                    "_id": 0,
                }
            }
        ]

        cursor = db['contenidos'].aggregate(pipeline, allowDiskUse=True)
        query_results = list(cursor)
        list_results.append(query_results[0])

    count = db['contenidos'].count_documents({})
    if len(list_results) == 0:
        list_contents = {'results': None}
    else:
        list_contents = {
            'total': count,
            'results': list_results
        }
    
    return list_contents