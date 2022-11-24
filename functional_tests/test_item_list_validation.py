from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.by import By


class ItemValidationTest(FunctionalTest):
    '''Тест на проверку элемента списка'''

    def test_add_empty_list_item(self):
        '''тест: нельзя отправить пустой элемент'''
        # Я зашел на домашнюю страницу и случайно отправил пустой элемент
        self.browser.get(self.live_server_url)
        self.input_box('')
        # Домашняя страница обновляется и появляется сообщение об ошибке
        self.wait_for(lambda : self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:invalid'))
        # Я ввожу необходимые значения в поле ввода, нажимаю Enter и все работает как надо, а ошибка исчезает
        self.input_box('Учиться')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:invalid'))
        self.wait_for_row_in_list_table('1: Учиться')

        # После этого я опять случайно нажимаю Enter на пустом поле ввода и снова появляется сообщение об ошибке
        self.input_box('')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:invalid'))
        # Это можно исправить введя в поле некий текст
        self.fail('Введи меня')

    def test_cannot_add_duplicate_items(self):
        '''тест: нельзя добавлять дублирующие элементы'''
        # Я захожу на домашнюю страницу и начинаю новый список
        self.browser.get(self.live_server_url)
        self.input_box('Купить молока')
        # Вижу что список начался и на нем появился первый элемент "Купить молока"
        self.wait_for_row_in_list_table('1: Купить молока')
        # Пытаюсь снова ввести "Купить молока"
        self.input_box('Купить молока')
        # И вижу предупреждение что нельзя добавлять дупликаты
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(by=By.CSS_SELECTOR, value='p.has_error').text,
                                               'Это уже есть в списке'))



