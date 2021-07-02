from handle.mongo import mongo
import json

def loginUser(email, hashSecure, publicHash):
    db = mongo.get_db()
    loginExitoso = False

    cursor = db['usuarios'].find_one({'Email': email}, projection={'_id':0})
    print(cursor)

    if cursor == None:
        loginExitoso = 'nomail'
    else:
        if cursor['Activated'] == True:
            if cursor['SecureHash'] == hashSecure and cursor['PublicHash'] == publicHash:
                loginExitoso = 'ok'
            else:
                loginExitoso = 'wrongpass'
        else:
            loginExitoso = 'inactive'

    resultJSON = {
        'loginState': loginExitoso
    }
    
    return resultJSON