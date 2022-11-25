from django.test import TestCase
from list.forms import ItemForm, ExistingListItemForm
from list.models import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, Item, List


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


class ExistingListItemFormTest(TestCase):
    '''тест: проверка элементов в существующем списке'''

    def test_form_renders_item_text_input(self):
        '''тест: форма отображает текстовый ввод элемента'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do"', form.as_p())

    def test_form_validation_for_blank_item(self):
        '''тест: валидация формы для пустых элементов'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        '''тест: проверка валидации формы для дубликатов'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins')
        form = ExistingListItemForm(for_list=list_, data={'text':'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
