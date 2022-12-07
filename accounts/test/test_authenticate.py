from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()

class Mock_Request:
    def __init__(self, token):
        self.GET = {'token':token}

class AuthenticationTest(TestCase):
    '''тесты для проверки аутентификации'''

    def test_returns_None_if_no_such_token(self):
        '''тест: с неправильным токеном возвращается None'''
        mock_request = Mock_Request('no-such-token')
        result = PasswordlessAuthenticationBackend().authenticate(mock_request)
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''тест: возвращается новый пользователь с правильным email если существует маркер'''
        email = 'example@mail.com'
        token = Token.objects.create(email=email)
        mock_request = Mock_Request(token.uid)
        user = PasswordlessAuthenticationBackend().authenticate(mock_request)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        '''тест: возвращается существующий пользователь с правильным email если существует маркер'''
        email = 'example@mail.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        mock_request = Mock_Request(token.uid)
        user = PasswordlessAuthenticationBackend().authenticate(mock_request)
        self.assertEqual(existing_user, user)


class GetUserTest(TestCase):
    '''тесты для проверки функции get_user нашего беспарольного процессора аутентификации'''

    def test_gets_user_by_email(self):
        '''тест: получение юзера по существующему email'''
        User.objects.create(email = 'another@mail.com')
        desired_user = User.objects.create(email='example@mail.com')
        found_user = PasswordlessAuthenticationBackend().get_user('example@mail.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_that_email(self):
        '''тест: возвращается None если не находится юзер по данному email'''
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('example@mail.com'))
