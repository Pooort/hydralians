import logging
import os
import time

from selenium import webdriver

from config import HEADLESS
from logging.handlers import RotatingFileHandler


def get_web_driver(headless=HEADLESS):

    chop = webdriver.ChromeOptions()

    if headless:
        chop.add_argument('--headless')
        chop.add_argument('--disable-gpu')
        chop.add_argument('--window-size=1280x1696')
        chop.add_argument('--ignore-certificate-errors')
        chop.add_argument('--disable-dev-shm-usage')
        chop.add_argument('--no-sandbox')

    file_path = os.path.dirname(os.path.realpath(__file__))

    chromedriver = os.path.join(file_path, 'chromedriver')
    driver = webdriver.Chrome(chromedriver, options=chop)
    return driver


def get_logger():
    logger = logging.getLogger('Main')

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/data.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    return logger


def wait_function(func, timeout_param=None):
    def inner_func(*args, **kwargs):
        timeout = 10 if timeout_param is None else timeout_param
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                duration = time.time() - start_time
                if duration > timeout:
                    raise ex
                time.sleep(0.5)
    return inner_func
