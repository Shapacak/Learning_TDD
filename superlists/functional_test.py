from selenium import webdriver
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
        self.fail('Закончить тест')

        #Здесь нам предлагается начать вести свой список дел
        #Наше первое дело это учить ЯП Python
        #Мы пишем его и нажимаем Enter
        #Теперь в списке появился пункт под номером 1 'Учить Python'
        #Текстовое поле все еще предлагает добавлять дела в список
        #Добавляем 'Тренировки на турнике'
        #Страница обновляется и теперь в списке два наших дела
        #Нам интересно, сохраняется ли наш список
        #Сайт генерирует для нас уникальный URL, и выводит для нас небольшой текст с объяснениями
        #Посещаем данный URL и видим что список на месте
        #Закрываем сайт


if __name__ == '__main__':
    unittest.main(warnings='ignore')