from handle.mongo import mongo
import json

def regUser(email, hashSecure, publicHash):
    db = mongo.get_db()
    regExitoso = False

    payload = {
        'Email': email,
        'SecureHash': hashSecure,
        'PublicHash': publicHash,
        'Activated': False,
        'MyList': [],
    }

    cursor = db['usuarios'].find_one({'Email': email}, projection={'Email':1, '_id':0})
    print(cursor)

    if cursor == None:
        result = db['usuarios'].insert_one(payload)
        regExitoso = result.acknowledged
    else:
        regExitoso = False

    resultJSON = {
        'success': regExitoso
    }
    
    return resultJSON