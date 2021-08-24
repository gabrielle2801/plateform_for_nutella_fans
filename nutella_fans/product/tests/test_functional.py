from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from nutella_fans.users_account.models import User

class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.user = User.objects.create(
            username='Xavier', email='xavier@email.com', password='gabi@1428')

    def test_search_product(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:8000')
        search_bar = driver.find_element_by_name("search_product")
        search_bar.clear()
        search_bar.send_keys("Biscuit")
        driver.implicitly_wait(10)
        search_bar.send_keys(Keys.RETURN)

    def test_login(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:8000/account/login/')
        driver.find_element_by_id('id_username').send_keys('Xavier')
        driver.find_element_by_name('password').send_keys('gabi@1428')
        driver.find_element_by_class_name('account-btn').click()

    def tearDown(self):
        self.driver.close()


'''
    def test_search_base_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000')
        heading1 = driver.find_element_by_class_name('text-uppercase')
        heading1.send_keys('DU GRAS OUI MAIS DE QUALITE !')
        driver.implicitly_wait(20)
        heading1.send_keys(Keys.RETURN)
'''
