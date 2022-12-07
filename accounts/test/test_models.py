from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib import auth
from accounts.models import Token

User = get_user_model()
AB_EMAIL = 'a@b.mail.com'


class UserModelTest(TestCase):
    '''тесты для модели пользователя'''

    def test_user_is_valid_with_email_only(self):
        '''тест: для создания пользователя необходима только электронная почта'''
        user = User.objects.create(email=AB_EMAIL)
        user.full_clean()

    def test_email_si_primary_key(self):
        '''тест: email является первичным ключем'''
        user = User.objects.create(email=AB_EMAIL)
        self.assertEqual(user.pk, AB_EMAIL)

    def test_no_problem_with_auth_login(self):
        '''тест: нет проблем с auth_login'''
        user = User.objects.create(email='example@mail.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)


class TokenModelTest(TestCase):
    '''тест модели маркера'''

    def test_links_user_with_auto_generated_uid(self):
        '''тест: при получении токена кажждый раз генирируется новый uid'''
        token1 = Token.objects.create(email=AB_EMAIL)
        token2 = Token.objects.create(email=AB_EMAIL)
        self.assertNotEqual(token1.uid, token2.uid)