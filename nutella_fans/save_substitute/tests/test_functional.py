from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from django.core import management
from django.core.management import call_command

options = webdriver.FirefoxOptions()
# options.headless = True


class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        """Summary
        """
        self.driver = webdriver.Firefox(options=options)
        call_command('load_functional_test_data')

    def test_signup(self):

        self.driver.get('http://127.0.0.1:8000/sign_up/')
        self.driver.find_element_by_id('id_username').send_keys('Gabrielle')
        self.driver.find_element_by_id(
            'id_email').send_keys('gabrielle@email.com')
        self.driver.find_element_by_id('id_password1').send_keys('12@test@12')
        self.driver.find_element_by_id('id_password2').send_keys('12@test@12')
        self.driver.find_element_by_class_name('account-btn').click()

    def test_add_favorite_list(self):

        self.driver.implicitly_wait(20)
        self.driver.get('http://127.0.0.1:8000/account/login/')
        # self.driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        self.driver.find_element_by_id('id_username').send_keys('Gabrielle')
        self.driver.find_element_by_name('password').send_keys('12@test@12')
        self.driver.find_element_by_class_name('account-btn').click()
        search_bar = self.driver.find_element_by_name("search_product")
        search_bar.send_keys("Biscuit")
        search_bar.send_keys(Keys.RETURN)
        # self.driver.get('%s%s' % (self.live_server_url,'/substitutes/104/'))
        self.driver.get('http://127.0.0.1:8000/substitutes/50')
        input_product = self.product_id
        input_substitute = self.substitute_id
        import ipdb
        ipdb.set_trace()
        self.driver.execute_script("arguments[0].value='50';", input_product)
        self.driver.execute_script(
            "arguments[0].value='48';", input_substitute)
        self.driver.find_element_by_name('btn-favorate').click()
        self.driver.get('http://127.0.0.1:8000/favorites_list/')


'''
    def test_favorite_delete(self):
        driver = self.driver
        # driver.implicitly_wait(20)
        driver.get('http://127.0.0.1:8000/account/login/')
        # driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        driver.find_element_by_id('id_username').send_keys('Xavier')
        driver.find_element_by_name('password').send_keys('gabi@1428')
        driver.find_element_by_class_name('account-btn').click()
        driver.get('http://127.0.0.1:8000/favorites_list/')
        driver.get('http://127.0.0.1:8000/delete_favorate/'), self.substitute_id
        driver.find_element_by_name('Confirm_btn').click()
'''
