from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page


class HomePageTest(TestCase):
    '''Тестируем домашнюю страницу'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: url-/ преобразуется в представление домашней станицы'''

        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница возвращает правильный html'''
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.endswith('</html>'))