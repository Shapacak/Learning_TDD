import os
#from config import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('./chromedriver/chromedriver.exe')
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for(self, fn):
        '''ожидание'''
        start_time = time.time()

        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, text_row):
        '''проверка на наличие текста в строках таблицы'''
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(text_row, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def input_box(self, text):
        '''вводим текст в поле ввода'''

        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

