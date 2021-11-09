from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from nutella_fans.users_account.models import User

options = webdriver.FirefoxOptions()
# options.headless = True
class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        """Summary
        """
        self.driver = webdriver.Firefox(options=options)
        self.user = User.objects.create(
            username='Xavier', email='xavier@email.com', password='gabi@1428')

    def test_favorite_delete(self):
        driver = self.driver
        # driver.implicitly_wait(20)
        driver.get('http://127.0.0.1:8000/account/login/')
        # driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        driver.find_element_by_id('id_username').send_keys('Xavier')
        driver.find_element_by_name('password').send_keys('gabi@1428')
        driver.find_element_by_class_name('account-btn').click()
        driver.get('http://127.0.0.1:8000/favorites_list/')
        # driver.get('%s%s' % (self.live_server_url, '/favorites_list/'))
        # driver.get('%s%s' % (self.live_server_url, '/delete_favorate/27'))
        driver.get('http://127.0.0.1:8000/delete_favorate/28')
        driver.find_element_by_name('Confirm_btn').click()

    def test_favorite_list(self):
        driver = self.driver
        # driver.implicitly_wait(20)
        driver.get('http://127.0.0.1:8000/account/login/')
        # driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        driver.find_element_by_id('id_username').send_keys('Xavier')
        driver.find_element_by_name('password').send_keys('gabi@1428')
        driver.find_element_by_class_name('account-btn').click()
        search_bar = driver.find_element_by_name("search_product")
        search_bar.send_keys("Biscuit")
        search_bar.send_keys(Keys.RETURN)
        # driver.get('%s%s' % (self.live_server_url, '/substitutes/50'))
        driver.get('http://127.0.0.1:8000/substitutes/50')
        input_product = driver.find_element_by_name('product_id')
        input_substitute = driver.find_element_by_name('substitute_id')
        driver.execute_script("arguments[0].value='50';", input_product)
        driver.execute_script("arguments[0].value='48';", input_substitute)
        driver.find_element_by_name('btn-favorate').click()
        # driver.get('%s%s' % (self.live_server_url, '/favorites_list/'))
        driver.get('http://127.0.0.1:8000/favorites_list/')
