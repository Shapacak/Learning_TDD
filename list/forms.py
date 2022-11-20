from django import forms
from list.models import Item


EMPTY_ITEM_ERROR = 'Вы не можете оставить это поле пустым'


class ItemForm(forms.ModelForm):
    '''форма для элемента списка'''

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do',
                'class': 'form-control input-lg',}),}
        error_messages = {'text': {'required': EMPTY_ITEM_ERROR}}

    item_text = forms.CharField(max_length=20,
                                widget=forms.fields.TextInput(attrs={'placeholder': 'Enter a to-do',
                                                                     'class': 'form-control input-lg'}),)