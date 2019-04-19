from pymongo import MongoClient

client = MongoClient()
db = client['hydralians']
collection = db['products']


class MongoRepo:

    @staticmethod
    def create(data):
        collection.update_one({'url': data['url']}, {"$set": data}, True)
        return collection.find_one({'url': data['url']})

    @staticmethod
    def create_product_url(data):
        collection = db['product_urls']
        collection.update_one({'url': data['url']}, {"$set": data}, True)
        return collection.find_one({'url': data['url']})

    @staticmethod
    def get_all_product_urls():
        collection = db['product_urls']
        return collection.find({})

    @staticmethod
    def read_all():
        return collection.find({})
