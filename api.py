from flask import Flask, request, jsonify
import json

from endpoints import contents as c
from endpoints import registro as reg
from endpoints import login as log
from endpoints import verification as ver

app = Flask(__name__)


@app.route('/contenidos', methods=['GET'])
def contents():
    pageNum = request.args.get('pageNum', 0)

    if request.method == 'GET':

        result = c.get(pageNum)

        return result
    
@app.route('/userReg', methods=['PUT'])
def userReg():
    email = request.json.get('email')
    hashSecure = request.json.get('hashSHA256')
    publicHash = request.json.get('publicHash')

    print(email, hashSecure, request.method)

    if request.method == 'PUT':

        result = reg.regUser(email, hashSecure, publicHash)

    return result

@app.route('/verification', methods=['PUT'])
def verification():
    publicHash = request.json.get('publicHash')

    print(publicHash, request.method)

    if request.method == 'PUT':

        result = ver.verification(publicHash)

    return result

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    hashSecure = request.json.get('hashSHA256')
    publicHash = request.json.get('publicHash')

    print(email, hashSecure, request.method)

    if request.method == 'POST':

        result = log.loginUser(email, hashSecure, publicHash)

    return result

@app.errorhandler(429)
def access429(error):
    return jsonify(
        {
            'Error'     : '429',
            'Msg'       : 'Too Many Requests.'
        }
    )

@app.errorhandler(405)
def error405(error):
    return jsonify(
        {
            'Error'     : '405',
            'Msg'       : 'Method Not Allowed.'
        }
    )

@app.errorhandler(500)
def error500(error):
    return jsonify(
        {
            'Error'     : '500',
            'Msg'       : 'Server Internal Error.'
        }
    )

@app.errorhandler(502)
def error502(error):
    return jsonify(
        {
            'Error'     : '502',
            'Msg'       : 'Bad Gateway.'
        }
    )

@app.errorhandler(404)
def error404(error):
    return jsonify(
        {
            'Error'     : '404',
            'Msg'       : 'Not Found.'
        }
    )

if __name__ == '__main__':
    app.run(debug=True)


