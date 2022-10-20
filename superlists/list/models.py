from django.db import models


class Lists(models.Model):
    pass


class Item(models.Model):
    text = models.CharField(max_length=50)
    list = models.ForeignKey(Lists, on_delete=models.CASCADE, default=None, null=True)