import datetime

from tqdm import tqdm

from downloader import download_data
from helpers import get_logger
from manager import Hydralians
from mongorepo import MongoRepo

logger = get_logger()

start_time = datetime.datetime.now()
logger.info('Script started at {}'.format(start_time))

with Hydralians() as hydralians:
    hydralians.make_order('32210260')

end_time = datetime.datetime.now()
logger.info('Script ended at {}'.format(end_time))
