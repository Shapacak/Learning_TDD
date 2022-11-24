from django import forms
from list.models import Item, EMPTY_ITEM_ERROR



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
