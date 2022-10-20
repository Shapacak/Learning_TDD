from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page
from list.models import Item, List


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
        new_list = Lists.objects.first()
        self.assertRedirects(response, f'/list/{new_list.id}/')


class NewItemTest(TestCase):
    '''тест нового элемента'''

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно ли сохранить элемент в существующий список'''

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/list/{correct_list.id}/add_item', data={'item_text':'A new item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        '''тест: переадресация на список'''

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/list/{correct_list.id}/add_item', data={'item_text':'Few item'})
        self.assertRedirects(response, f'/list/{correct_list.id}/')

class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_uses_list_template(self):
        '''тест: используется шаблон списка'''

        list_ = List.objects.create()
        response = self.client.get(f'/list/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        '''тест: передается правильный шаблон списка'''

        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/list/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        '''тест: отображаются элементы только этого списка'''

        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other 1', list=other_list)
        Item.objects.create(text='other 2', list=other_list)

        response = self.client.get(f'/list/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 1')
        self.assertNotContains(response, 'other 1')
        self.assertNotContains(response, 'other 2')


class ListAndItemModelsTests(TestCase):
    '''Тестируем модель элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения списка'''
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        saved_first_item = saved_items[0]
        saved_second_item = saved_items[1]

        self.assertEqual('The first (ever) list item', saved_first_item.text)
        self.assertEqual(saved_first_item.list, list_)
        self.assertEqual('Item the second', saved_second_item.text)
        self.assertEqual(saved_second_item.list, list_)