from selenium.common.exceptions import TimeoutException

from config import email, password
from helpers import get_web_driver

from tqdm import tqdm

#https://www.hydralians.fr/piscine/structure-et-hydraulique/pieces-a-sceller-piscine.html?limit=100&p=2
class Hydralians:

    url = 'https://www.hydralians.fr/'

    def __init__(self):
        driver = get_web_driver()
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(5)
        driver.set_window_size(1920, 1080)
        self.driver = driver

    def make_login(self):
        self.driver.get('https://www.hydralians.fr/customer/account/login/')
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('send2').click()

    def get_category_hrefs(self):
        self.driver.get('https://www.hydralians.fr/site-map')
        menu_hrefs = [el.get_attribute('href') for el in self.driver.find_elements_by_xpath('//a[@class="menu-sp"]')]
        category_hrefs = []
        menu_bar = tqdm(total=len(menu_hrefs))
        menu_bar.set_description(desc='Menu items')
        for menu_href in menu_hrefs:
            menu_bar.update()
            try:
                self.driver.get(menu_href)
            except TimeoutException:
                pass
            try:
                current_category_hrefs = [el.get_attribute('href') for el in self.driver.find_elements_by_xpath('//div[@class="sub-categ"]/h5/a')]
                category_hrefs.extend(current_category_hrefs)
            except TimeoutException:
                pass
        menu_bar.close()
        return category_hrefs

    def get_item_hrefs(self, category_hrefs):
        item_hrefs = []
        category_bar = tqdm(total=len(category_hrefs))
        category_bar.set_description(desc='Categories')
        for category_href in category_hrefs:
            category_bar.update()
            page = 1
            while True:
                try:
                    self.driver.get('{}?limit=100&p={}'.format(category_href, page))
                except TimeoutException:
                    pass
                try:
                    current_item_hrefs = [el.get_attribute('href') for el in self.driver.find_elements_by_xpath('//h2[@class="product-name"]/a')]
                except TimeoutException:
                    pass
                item_hrefs.extend(current_item_hrefs)

                try:
                    site_pages = [el.text for el in
                                  self.driver.find_elements_by_xpath('//div[@class="pages"]/ol/li')]
                except:
                    site_pages = []
                page += 1
                if str(page) not in site_pages:
                    break
        category_bar.close()
        return item_hrefs

    def __enter__(self):
        self.make_login()
        category_hrefs = self.get_category_hrefs()
        item_hrefs = self.get_item_hrefs(category_hrefs)
        with open('urls.txt', 'w') as f:
            for item_href in item_hrefs:
                f.write('{}\n'.format(item_href))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
