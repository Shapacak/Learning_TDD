from django.test import TestCase
from list.forms import ItemForm
from list.models import EMPTY_ITEM_ERROR, Item, List


class ItemFormTest(TestCase):
    '''проверка формы для элемента списка'''

    def test_form_case(self):
        '''тест: форма отображает текстовое поле'''
        form = ItemForm()
        self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_css_and_css_classes(self):
        '''тест: проверка на наличие placeholder и css-классов'''
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_validation_for_blank_items(self):
        '''тест: валидация формы для пустых элементов'''
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_ITEM_ERROR])

    def test_home_page_uses_item_form(self):
        '''тест: используется ли на главной странице ItemForm'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_form_save_handles_saving_to_a_list(self):
        '''тест: метод save формы обрабатывает сохранение в список'''
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'to do'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'to do')
        self.assertEqual(new_item.list, list_)