from django.test import TestCase
from django.urls import resolve
from list.views import home_page


class HomePageTest(TestCase):
    '''Тестируем домашнюю страницу'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: url-/ преобразуется в представление домашней станицы'''

        found = resolve('/')
        self.assertEqual(found.func, home_page)