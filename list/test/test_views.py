from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page
from list.models import Item, List, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from list.forms import ItemForm, ExistingListItemForm
from unittest import skip


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

        response = self.client.post('/list/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        '''тест: переадресация после post-запроса'''

        response = self.client.post('/list/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/list/{new_list.id}/')


class NewItemTest(TestCase):
    '''тест нового элемента'''

    def test_for_invalid_input_render_home_page_template(self):
        '''тест: ошибки возвращают на главную страницу'''
        response = self.client.post('/list/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validations_errors_shown_on_home_page(self):
        '''тест: ошибки валидации выводятся на главной странице'''
        response = self.client.post('/list/new', data={'text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_inpud_passes_form_template(self):
        '''тест: форма передается в шаблон после недопустимого элемента'''
        response = self.client.post('/list/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_item_ared_saved(self):
        '''тест: сохраняются ли недопустимые элементы списка'''
        self.client.post('/list/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    '''тест представления списка'''

    def post_invalid_input(self):
        '''отправляет недопустимый ввод'''
        list_ = List.objects.create()
        return self.client.post(f'/list/{list_.id}/', data={'text': ''})

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

        self.client.post(f'/list/{correct_list.id}/', data={'text': 'A new item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        '''тест: переадресация на список'''

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/list/{correct_list.id}/', data={'text':'Few item'})
        self.assertRedirects(response, f'/list/{correct_list.id}/')

    def test_validation_errors_end_up_lists_page(self):
        '''тест: ошибки валидации оканчиваются на странице списков'''

        list_ = List.objects.create()
        response = self.client.post(f'/list/{list_.id}/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_display_item_form(self):
        '''тест отображения формы'''
        list_ = List.objects.create()
        response = self.client.get(f'/list/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        '''тест: при недопустимом вводе ничего не сохраняется в бд'''
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_inputs_render_list_template(self):
        '''тест: при недопустимом вводе отображается шаблон списка'''
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест: при недопустимом вводе форма передается в шаблон'''
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        '''тест: прои недопустимом вводе на экране отображается ошибка'''
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_duplicate_item_validation_errors_end_on_lists_page(self):
        '''тест: ошибки валидации дупликатов заканчиваются на странице списков'''
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='some text')
        response = self.client.post(f'/list/{list_.id}/', data={'text': 'some text'})
        self.assertContains(response, DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)