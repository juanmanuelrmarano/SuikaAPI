from handle.mongo import mongo
import json

def get(publicHash,idcontenido):
    db = mongo.get_db()
    success = {'success': True}

    print(publicHash, idcontenido)

    cursorMyList = db['usuarios'].find_one({'PublicHash': publicHash})

    if cursorMyList == None:
        success = {'success': False}

    print(cursorMyList)

    mylistFinal = []
    for item in cursorMyList['MyList']:
        mylistFinal.append(item)
    mylistFinal.append(idcontenido)

    print(mylistFinal)

    payload = {
        'MyList' : mylistFinal
    }
    cursorAdd = db['usuarios'].update_one({'PublicHash': publicHash}, {u'$set' : payload}, upsert= True)

    if cursorAdd.acknowledged == False:
        success = {'success': False}
    
    return success