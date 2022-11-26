from django import forms
from django.core.exceptions import ValidationError
from list.models import Item, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR


class ItemForm(forms.ModelForm):
    '''форма для элемента списка'''

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {'text': forms.fields.TextInput(
            attrs={'placeholder': 'Enter a to-do','class': 'form-control input-lg'})}
        error_messages = {'text': {'required': EMPTY_ITEM_ERROR}}


class ExistingListItemForm(ItemForm):
    '''форма элемента списка для уже существуещего списка'''

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        '''валидация уникальности'''
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)