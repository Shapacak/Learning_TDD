from django.test import TestCase
from unittest.mock import patch, call
import accounts.views
from accounts.models import Token


@patch('accounts.views.auth')
class SendLoginEmailViewTest(TestCase):
    '''тест представления которое отправляет приглашение на почту'''

    def test_redirect_to_home_page(self, mock_auth):
        '''тест: после отправки email представление переадресовывает нас на домашнюю страницу'''
        response = self.client.post('/accounts/send_login_email', data={'email': 'example@mail.com'})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail, mock_auth):
        '''тест: отправляется сообщение на адресс из метода post'''
        self.client.post('/accounts/send_login_email', data={'email':'example@mail.com'})
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlist')
        self.assertEqual(to_list, ['example@mail.com'])

    def test_add_success_messages(self, mock_auth):
        '''тест: добавляется сообщение об успехе'''
        response = self.client.post('/accounts/send_login_email', data={'email':'example@mail.com'}, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 'Проверьте свою почту, мы отправили Вам ссылку для входа на сайт')
        self.assertEqual(message.tags, 'success')

    def test_redirects_to_home_page(self, mock_auth):
        '''тест: переадресуется на домашнюю страницу'''
        response = self.client.get('/accounts/login?token=qqbc123')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self, mock_auth):
        '''тест: создается токен связанный с электронной почтой'''
        self.client.post('/accounts/send_login_email', data={'email':'example@mail.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'example@mail.com')

    @patch('accounts.views.send_mail')
    def test_send_link_to_login_using_token_uid(self, mock_send_mail, mock_auth):
        '''тест: отсылается ссылка на вход в систему с ипользованием uid маркера'''
        self.client.post('/accounts/send_login_email', data={'email':'example@mail.com'})
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_mail, to_lost), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        '''тест: вызывается authenticate с uid из GET-запроса'''
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.authenticate.call_args,
                         call(request=response.wsgi_request))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        '''тест: вызывается auth_login с пользователем, если такой имеется'''
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.login.call_args,
                         call(response.wsgi_request, mock_auth.authenticate.return_value))

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        '''тест: не регистрируемся в системе если пользователь не авторизован'''
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.login.called, False)

