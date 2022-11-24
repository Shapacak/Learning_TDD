from django.test import TestCase
from django.core.exceptions import ValidationError
from list.models import List, Item


class ListModelTests(TestCase):
    '''Тесты для модели List'''

    def test_get_absolute_url(self):
        '''тест: получен абсолютный url'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/list/{list_.id}/')


class ItemModelTests(TestCase):
    '''Тесты для модели Item'''

    def test_cannot_save_empty_list_item(self):
        '''тест: нельзя сохранить пустой элемент'''
        list_ = List()
        list_.save()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        '''тест: дупликаты в одном и том же листе недопустимы'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_can_save_some_item_to_different_list(self):
        '''тест: одинаковые элементы можно сохранить в разных листах'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()   # не должен вызывать ошибку

    def test_list_orderings(self):
        '''тест: проверка упорядочивания элементов списка'''
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='1')
        item2 = Item.objects.create(list=list_, text='2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        '''тест: строковое представление'''
        item = Item.objects.create(text='Some text')
        self.assertEqual(str(item), 'Some text')

    def test_default_text(self):
        '''тест: заданный по умолчанию текст'''
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        '''тест: элемент связан со списком'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertEqual(item.list, list_)
        self.assertEqual(item, list_.item_set.first())