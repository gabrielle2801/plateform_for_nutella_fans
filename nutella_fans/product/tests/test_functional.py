from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from nutella_fans.users_account.models import User

class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.user = User.objects.create(
            username=user, email='gabrielle@email.com', password='12test12')

    def test_search_base_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000')
        heading1 = driver.find_element_by_tag_name('h1')
        heading1.send_keys('Du gras oui, mais de qualité !')
        heading1.send_keys(Keys.RETURN)

    def test_search_product(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000')
        search_bar = driver.find_element_by_name("search_product")
        search_bar.clear()
        search_bar.send_keys("Biscuit")
        search_bar.send_keys(Keys.RETURN)

    def tearDownClass(self):
        self.driver.close()

    def test_login(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000')
