from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import email, password
from helpers import get_web_driver, wait_function

from tqdm import tqdm


class Hydralians:

    url = 'https://www.hydralians.fr/'

    def __init__(self):
        driver = get_web_driver()
        driver.set_page_load_timeout(5)
        self.driver = driver

    def get_item_data(self, url):
        self.driver.get(url)

        @wait_function
        def get_price(self):
            return self.driver.find_element_by_xpath('//span[@class="regular-price"]').text

        # try:
        #     price_el = WebDriverWait(self.driver, 240).until(
        #         EC.presence_of_element_located((By.XPATH, '//span[@class="regular-price"]')))
        #     price = price_el.text
        # except Exception as ex:
        #     price = ''
        try:
            price = get_price(self)
        except:
            price = ''
        product_name = self.driver.find_element_by_xpath('//h1[@class="product-name"]').text
        product_brand = self.driver.find_element_by_xpath('//span[@class="product-brand"]').text
        ref = self.driver.find_element_by_xpath('//div[@class="ref"]').text
        codag = self.driver.find_element_by_xpath('//div[@class="codag"]').text
        try:
            description = self.driver.find_element_by_xpath('//div[@class="std"]').text
        except:
            description = ''
        try:
            seq = self.driver.find_element_by_xpath('//div[@class="seq"]').text
        except:
            seq = ''
        image_urls = [el.get_attribute('src') for el in self.driver.find_elements_by_xpath('//div[@class="product-main-container grid-full"]//div[@class="viewport"]//img')]
        doc_data = [{'name': el.text, 'url': el.get_attribute('href')} for el in self.driver.find_elements_by_xpath('//div[@class="documents-content"]//a')]
        try:
            tax = self.driver.find_element_by_id('tax-deee-eco').text
        except:
            tax = ''
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            spec_el = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@href="#specifications"]/parent::*')))
            spec_el.click()
            spec = self.driver.find_element_by_id('product-attribute-specs-table').text
        except:
            spec = ''

        return {
            'url': url,
            'product_name': product_name,
            'product_brand': product_brand,
            'ref': ref,
            'codag': codag,
            'description': description,
            'seq': seq,
            'price': price,
            'image_urls': image_urls,
            'doc_data': doc_data,
            'spec': spec,
            'tax': tax
        }

    def make_login(self):
        self.driver.get('https://www.hydralians.fr/customer/account/login/')
        #self.driver.set_window_size(1920, 1080)
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'send2'))).click()

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
        self.driver.set_page_load_timeout(30)
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
                    item_hrefs.extend(current_item_hrefs)
                except TimeoutException:
                    pass

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
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def make_order(self, codag):
        self.driver.find_element_by_id('search').send_keys(codag)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        @wait_function
        def click_order_button():
            self.driver.find_element_by_id('addToCart_{}'.format(codag)).click()
        click_order_button()
