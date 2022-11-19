from django.test import TestCase
from django.core.exceptions import ValidationError
from list.models import List, Item


class ListAndItemModelsTests(TestCase):
    '''Тестируем модель элемента списка'''

    def test_cannot_save_empty_list_item(self):
        '''тест: нельзя сохранить пустой элемент'''
        list_ = List()
        list_.save()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

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