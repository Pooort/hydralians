from pymongo import MongoClient

from mongorepo import MongoRepo
from pprint import pprint

client = MongoClient()
db = client['hydralians']
collection = db['products']

diff_counter = 0

for product in MongoRepo.read_all():
    if product.get('diff') and product.get('diff').get('old') != product.get('diff').get('new'):
        pprint(product['diff'])
        diff_counter += 1

print(diff_counter)