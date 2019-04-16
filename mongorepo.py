from pymongo import MongoClient

client = MongoClient()
db = client['hydralians']
collection = db['products']


class MongoRepo:

    @staticmethod
    def create(data):
        collection.update_one({'url': data['url']}, {"$set": data}, True)

    @staticmethod
    def read_all():
        return collection.find({})

