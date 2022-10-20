from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    '''Тест нового посетителя'''

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('../chromedriver/chromedriver.exe')

    def tearDown(self) -> None:
        self.browser.quit()

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

    def test_can_start_a_list_for_one_user(self):
        '''тест: можно начать список для одного пользователя'''
        #Нам необходимо онлайн приложение для списка дел
        #Заходим на него
        self.browser.get(self.live_server_url)

        #Его заголовок гласит нам To-Do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('To-Do', header_text)

        #Здесь нам предлагается начать вести свой список дел
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do')

        #Наше первое дело это учить ЯП Python
        #Мы пишем его и нажимаем Enter
        self.input_box('Учить Python')

        #Теперь в списке появился пункт под номером 1 'Учить Python'
        self.wait_for_row_in_list_table('1: Учить Python')

        #Текстовое поле все еще предлагает добавлять дела в список
        #Добавляем 'Тренировки на турнике'
        self.input_box('Тренировки на турнике')

        #Страница обновляется и теперь в списке два наших дела
        self.wait_for_row_in_list_table('1: Учить Python')
        self.wait_for_row_in_list_table('2: Тренировки на турнике')
        #Нам интересно, сохраняется ли наш список
        #Сайт генерирует для нас уникальный URL, и выводит для нас небольшой текст с объяснениями
        #Посещаем данный URL и видим что список на месте
        #Закрываем сайт

    def test_multiple_users_can_start_list_at_different_url(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        #Я хочу начать новый список
        self.browser.get(self.live_server_url)
        self.input_box('Учить Python')
        self.wait_for_row_in_list_table('1: Учить Python')
        my_url = self.browser.current_url

        #Я вижу что мой список имеет уникальный url
        self.assertRegex(my_url, '/list/.+/')

        #Теперь новый пользователь приходит на сайт

        ##Мы используем новый сеанс браузера, тем самым обеспечивая, что бы никакая информация
        ##других пользователей не прошла через cookie и пр.

        self.browser.quit()
        self.browser = webdriver.Chrome('../chromedriver/chromedriver.exe')

        #Он посещает домашнюю страницу и не видит там списков от других пользователей
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('1: Учить Python', page_text)
        self.assertNotIn('2: Тренировки на турнике', page_text)

        #Теперь он начинает свой собственный список
        self.input_box('Купить молоко')
        self.wait_for_row_in_list_table('1: Купить молоко')

        #Получает свой собственный уникальный url, и он отличается от нашего
        other_url = self.browser.current_url
        self.assertRegex(other_url, '/list/.+/')
        self.assertNotEqual(my_url, other_url)

        #И опять таки ни одного пункта из моего списка
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('1:Учить Python', page_text)
        self.assertNotIn('2: Тренировки на турнике', page_text)
        self.assertIn('1: Купить молоко', page_text)

        #И мы оба довольные идем спать

    def test_layout_and_styling(self):
        '''тест: проверяем макет и оформление'''
        
        #Я решил открыть наш сайт
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,786)

        #Наше поле ввода находится по центру
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(input_box.location['x']+input_box.size['width']/2, 512, delta=10)

        #Я ввожу свое следующее дело и вижу что поле ввода все так же остается по центру
        self.input_box('testing')
        self.wait_for_row_in_list_table('testing')
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)

