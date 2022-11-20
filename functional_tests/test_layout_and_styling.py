from .base import FunctionalTest
from selenium.webdriver.common.by import By


class LayoutAndStylingTest(FunctionalTest):
    '''Тест макета и стилей'''

    def test_layout_and_styling(self):
        '''тест: проверяем макет и оформление'''

        # Я решил открыть наш сайт
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024 ,786)

        # Наше поле ввода находится по центру
        input_box = self.browser.find_element(by=By.ID, value='id_text')
        self.assertAlmostEqual(input_box.location['x' ] +input_box.size['width' ] /2, 512, delta=10)

        # Я ввожу свое следующее дело и вижу что поле ввода все так же остается по центру
        self.input_box('testing')
        self.wait_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element(by=By.ID, value='id_text')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)

