from pymongo import MongoClient

from helpers import logger

client = MongoClient()
db = client['hydralians']
collection = db['products']


def get_dicts_diff(old_dict, new_dict):
    result = {'old': {}, 'new': {}}
    all_keys = list(old_dict.keys())
    all_keys.extend(list(new_dict.keys()))
    all_keys.remove('_id')
    for key in set(all_keys):
        if not (key in old_dict and key in new_dict) or old_dict.get(key) != new_dict.get(key):
            result['old'][key] = old_dict.get(key)
            result['new'][key] = new_dict.get(key)
    return result


class MongoRepo:

    @staticmethod
    def create(data):
        existed_item = collection.find_one({'url': data['url']})
        if existed_item:
            data['diff'] = get_dicts_diff(existed_item, data)
            logger.info(data['diff'])
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
