from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    '''Тест нового посетителя'''

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('../chromedriver/chromedriver.exe')

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_at_later(self):
        '''тест: можно начать список и получить его позже'''
        #Нам необходимо онлайн приложение для списка дел
        #Заходим на него
        self.browser.get('http://localhost:8000')

        #Его заголовок гласит нам To-Do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('To-Do', header_text)

        #Здесь нам предлагается начать вести свой список дел
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do ')

        #Наше первое дело это учить ЯП Python
        inputbox.send_keys('Учить python')

        #Мы пишем его и нажимаем Enter
        inputbox.send_keys(keys.Enter)
        time.sleep(1)

        #Теперь в списке появился пункт под номером 1 'Учить Python'
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertTrue(any(row.text == '1: Учить Python' for row in rows))

        #Текстовое поле все еще предлагает добавлять дела в список
        self.fail()
        #Добавляем 'Тренировки на турнике'
        #Страница обновляется и теперь в списке два наших дела
        #Нам интересно, сохраняется ли наш список
        #Сайт генерирует для нас уникальный URL, и выводит для нас небольшой текст с объяснениями
        #Посещаем данный URL и видим что список на месте
        #Закрываем сайт


if __name__ == '__main__':
    unittest.main(warnings='ignore')