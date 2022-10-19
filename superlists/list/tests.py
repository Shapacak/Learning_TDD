from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page
from list.models import Item


class HomePageTest(TestCase):
    '''Тестируем домашнюю страницу'''

    def test_home_page_returns_correct_html(self):
        '''тест: используется шаблон для домашней страницы'''

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить POST-запрос'''

        response = self.client.post('/list/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        '''тест: переадресация после post-запроса'''

        response = self.client.post('/list/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/list/imba_list/')


class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''

        response = self.client.get('/list/imba_list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        '''тест: просмотр всех элементов списка'''

        item_1 = Item.objects.create(text='item 1')
        item_2 = Item.objects.create(text='item 2')
        response = self.client.get('/list/imba_list/')
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 1')


class ItemModelTest(TestCase):
    '''Тестируем модель элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения списка'''

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        saved_first_item = saved_items[0]
        saved_second_item = saved_items[1]

        self.assertEqual('The first (ever) list item', saved_first_item.text)
        self.assertEqual('Item the second', saved_second_item.text)