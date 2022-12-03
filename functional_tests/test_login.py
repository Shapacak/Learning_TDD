from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from .base import FunctionalTest


TEST_EMAIL = 'example@mail.com'
SUBJECT = 'Your login link for Superlist'


class LoginTest(FunctionalTest):
    '''тест регистрации в системе'''

    def test_can_get_email_link_to_login(self):
        '''тест: можно получить ссылку дла регистрации по почте'''
        # Я захожу на наш сайт суперсписков и замечаю новый элемент "Войти"
        # Он предлагает мне ввести свой email для этого
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value='email').send_keys(TEST_EMAIL)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)

        # Появляется сообщение что письмо было выслано на мою электронную почту
        self.wait_for(lambda : self.assertIn('Письмо отправлено',
                                             self.browser.find_element(by=By.TAG_NAME, value='body').text))

        # Я проверяю свою почту и нахожу там письмо
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит ссылку на url адресс
        self.assertIn('Проверьте свою электронную почту, там вы найдете сообщение с сылкой для входа на сайт',
                      self.browser.find_element(by=By.TAG_NAME, value='body').text)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            print(f'not found url in {email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Я нажимаю на ссылку
        self.browser.get(url)

        # Я зарегистрирован в системе
        self.wait_for(lambda : self.browser.find_element(by=By.LINK_TEXT,value='Log out'))
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
