from pymongo import MongoClient

class Mongo():
    def __init__(self):
        self.client = None

    def connect(self):
        self.client = MongoClient(host='mongodb+srv://suika:VolkswaguenGol2001@suikadata.rerjq.mongodb.net/admin?replicaSet=atlas-vb3vsy-shard-0&readPreference=primary&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1')
        return self.client

    def get_db(self, db='suika_api'):
        if not self.client:
            self.connect()

        return self.client[db]


mongo = Mongo()
