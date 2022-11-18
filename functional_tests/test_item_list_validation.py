from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.by import By


class ItemValidationTest(FunctionalTest):
    '''Тест на проверку элемента списка'''

    @skip
    def test_add_empty_list_item(self):
        '''тест: нельзя отправить пустой элемент'''
        # Я зашел на домашнюю страницу и случайно отправил пустой элемент
        self.browser.get(self.live_server_url)
        self.input_box('')
        # Домашняя страница обновляется и появляется сообщение об ошибке
        error_message = self.browser.find_element(by=By.ID, value='id_error_message').text
        self.assertEqual('Сначала введите текст', error_message)
        # Я ввожу необходимые значения в поле ввода, нажимаю Enter и все работает как надо
        self.input_box('Учиться')
        self.wait_for_row_in_list_table('1: Учиться')
        # После этого я опять случайно нажимаю Enter на пустом поле ввода и снова появляется сообщение об ошибке
        self.input_box('')
        error_message = self.browser.find_element(by=By.ID, value='id_error_message').text
        self.assertEqual('Сначала введите текст', error_message)
        # Это можно исправить введя в поле некий текст
        self.fail('Введи меня')


