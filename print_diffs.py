from pymongo import MongoClient

from mongorepo import MongoRepo
from pprint import pprint

client = MongoClient()
db = client['hydralians']
collection = db['products']

for product in MongoRepo.read_all():
    if product.get('diff') and product.get('diff').get('old') != product.get('diff').get('new'):
        pprint(product['diff'])
