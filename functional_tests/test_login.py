from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import os
import poplib
import time
from .base import FunctionalTest
from config.config import set_gmail_password

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    '''тест регистрации в системе'''

    def wait_for_email(self, test_email, subject):
        '''ожидание эллектронного сообщения через POP3'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GMAIL_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count-10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                    else:
                        time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_login(self):
        '''тест: можно получить ссылку дла регистрации по почте'''
        if self.staging_server:
            TEST_EMAIL = 'Shapacakbalanar@gmail.com'
        else:
            TEST_EMAIL = 'example@mail.com'
        # Я захожу на наш сайт суперсписков и замечаю новый элемент "Войти"
        # Он предлагает мне ввести свой email для этого
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value='email').send_keys(TEST_EMAIL)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)

        # Появляется сообщение что письмо было выслано на мою электронную почту
        self.wait_for(lambda : self.assertIn('Проверьте свою почту, мы отправили Вам ссылку для входа на сайт',
                                             self.browser.find_element(by=By.TAG_NAME, value='body').text))

        # Я проверяю свою почту и нахожу там письмо
        body = self.wait_for_email(TEST_EMAIL, SUBJECT)

        # Оно содержит ссылку на url адресс
        self.assertIn('Проверьте свою почту, мы отправили Вам ссылку для входа на сайт',body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'not found url in {body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Я нажимаю на ссылку
        self.browser.get(url)

        # Я зарегистрирован в системе
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Теперь я хочу выйти из системы
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()

        # И я вышел из системы
        self.wait_to_be_logged_out(TEST_EMAIL)
        self.assertIn('Вы вышли из системы',
                      self.browser.find_element(by=By.TAG_NAME, value='body').text)
