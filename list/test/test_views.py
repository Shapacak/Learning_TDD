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

        response = self.client.post('/list/new', data={'id_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        '''тест: переадресация после post-запроса'''

        response = self.client.post('/list/new', data={'id_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/list/{new_list.id}/')


class NewItemTest(TestCase):
    '''тест нового элемента'''

    def test_validation_error_are_sent_back_to_home_page_template(self):
        '''тест: ошибки возвращают на главную страницу'''
        response = self.client.post('/list/new', data={'id_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'Сначала введите текст'
        self.assertContains(response, expected_error)

    def test_invalid_list_item_ared_saved(self):
        '''тест: сохраняются ли недопустимые элементы списка'''
        self.client.post('/list/new', data={'id_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест: можно ли сохранить элемент в существующий список'''

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/list/{correct_list.id}/', data={'id_text':'A new item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        '''тест: переадресация на список'''

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/list/{correct_list.id}/', data={'id_text':'Few item'})
        self.assertRedirects(response, f'/list/{correct_list.id}/')

    def test_validation_errors_end_up_lists_page(self):
        '''тест: ошибки валидации оканчиваются на странице списков'''

        list_ = List.objects.create()
        response = self.client.post(f'/list/{list_.id}/', data={'id_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        error_message = 'Сначала введите текст'
        self.assertContains(response, error_message)