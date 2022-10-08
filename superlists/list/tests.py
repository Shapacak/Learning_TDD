from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page


class HomePageTest(TestCase):
    '''Тестируем домашнюю страницу'''

    def test_home_page_returns_correct_html(self):
        '''тест: используется шаблон для домашней страницы'''

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить POST-запрос'''

        response = self.client.post('/', data={'item_text':'A new list item'})
        self.assertIn('A new list item', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'home.html')