from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Token(models.Model):
    '''маркер'''

    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    '''менеджер пользователя списка'''

    def create_user(self, email):
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email=email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    '''Пользователь списка'''
    email = models.EmailField(primary_key=True)
    is_stuff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email']

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'Shapacakbalanar@gmail.com'

    @property
    def is_active(self):
        return True

    def __str__(self):
        return self.email

    class DoesNotExist:
        pass