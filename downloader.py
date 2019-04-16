import os
import urllib.request
from tqdm import tqdm

from mongorepo import MongoRepo

bar = tqdm()


def download_file(dir_name, file_name, file_url):
    dir_path = os.path.join('files', dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filepath = os.path.join(dir_path, file_name)
    if os.path.exists(filepath):
        return
    urllib.request.urlretrieve(file_url, filepath)


for document in MongoRepo.read_all():
    item_id = str(document['_id'])

    for image_url in document['image_urls']:
        file_name = image_url.rsplit('/', 1)[1]
        download_file(item_id, file_name, image_url)

    for file_data in document['doc_data']:
        download_file(item_id, '{}.pdf'.format(file_data['name']), file_data['url'])
