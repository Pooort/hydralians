import datetime

from tqdm import tqdm

from csvrepo import CsvRepo
from downloader import download_data
from helpers import get_logger
from manager import Hydralians
from mongorepo import MongoRepo

logger = get_logger()

start_time = datetime.datetime.now()
logger.info('Order script started at {}'.format(start_time))

with Hydralians() as hydralians:
    for codag, quantity in CsvRepo.get_codags():
        hydralians.make_order(codag, quantity)

end_time = datetime.datetime.now()
logger.info('Order script ended at {}'.format(end_time))
