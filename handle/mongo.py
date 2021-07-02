from pymongo import MongoClient

class Mongo():
    def __init__(self):
        self.client = None

    def connect(self):
        self.client = MongoClient()
        return self.client

    def get_db(self, db='suika_api'):
        if not self.client:
            self.connect()

        return self.client[db]


mongo = Mongo()
