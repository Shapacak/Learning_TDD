import uuid
from django.db import models
from django.core.exceptions import ObjectDoesNotExist



class User(models.Model):
    '''модель пользователя'''
    email = models.EmailField(unique=True, primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = False

    class DoesNotExists(ObjectDoesNotExist):
        pass


class Token(models.Model):
    '''модель генирирующая uid'''
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)

    class DoesNotExists(ObjectDoesNotExist):
        pass