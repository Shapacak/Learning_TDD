from django.db import models
from django.urls import reverse


EMPTY_ITEM_ERROR = 'Вы не можете оставить это поле пустым'
DUPLICATE_ITEM_ERROR = 'Этот элемент уже есть в списке'


class List(models.Model):
    '''список'''

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(error_messages={'required': EMPTY_ITEM_ERROR, 'unique': DUPLICATE_ITEM_ERROR})
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.text
    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')