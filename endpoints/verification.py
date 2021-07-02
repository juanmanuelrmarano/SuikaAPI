from handle.mongo import mongo
import json

def verification(publicHash):
    db = mongo.get_db()
    exitoso = None

    print(publicHash)

    cursor = db['usuarios'].find_one({'PublicHash': publicHash}, projection={'_id':0})
    print(cursor)

    filter = {'PublicHash': publicHash}
    newvalues = { "$set": { 'Activated': True } }

    if cursor == None:
        exitoso = False
    else:
        if cursor['Activated'] == False:
            result = db['usuarios'].update_one(filter, newvalues)
            exitoso = result.acknowledged

    resultJSON = {
        'success': exitoso
    }

    print(resultJSON)
    
    return resultJSON