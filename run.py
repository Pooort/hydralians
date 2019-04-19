import datetime

from tqdm import tqdm

from downloader import download_data
from helpers import get_logger
from manager import Hydralians
from mongorepo import MongoRepo

#https://www.hydralians.fr/bouche-refoulement-hydro-inverse-beton.html
# with Hydralians() as hydralians:
#     item_hrefs = MongoRepo.get_all_product_urls()
#     items_bar = tqdm(total=item_hrefs.count())
#     items_bar.set_description(desc='Items')
#     for item_data in item_hrefs:
#         try:
#             item_data = hydralians.get_item_data(item_data['url'])
#         except TimeoutException:
#             continue
#         item_data = MongoRepo.create(item_data)
#         download_data(item_data)

logger = get_logger()

start_time = datetime.datetime.now()
logger.info('Script started at {}'.format(start_time))

with Hydralians() as hydralians:
    category_hrefs = hydralians.get_category_hrefs()
    item_hrefs = hydralians.get_item_hrefs(category_hrefs)
    logger.info('Items to parse: {}'.format(len(item_hrefs)))
    # for item_href in item_hrefs:
    #     MongoRepo.create_product_url({'url': item_href})
    items_bar = tqdm(total=len(item_hrefs))
    items_bar.set_description(desc='Items')
    for item_href in item_hrefs:
        item_data = hydralians.get_item_data(item_href)
        item_data = MongoRepo.create(item_data)
        download_data(item_data)
    items_bar.close()

end_time = datetime.datetime.now()
logger.info('Script ended at {}'.format(end_time))
