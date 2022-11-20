from django.test import TestCase
from list.forms import ItemForm, EMPTY_ITEM_ERROR


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
        self.assertEqual(form.errors['text'],
                         [EMPTY_ITEM_ERROR])

    def test_home_page_uses_item_form(self):
        '''тест: используется ли на главной странице ItemForm'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
