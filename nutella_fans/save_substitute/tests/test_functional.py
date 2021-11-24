from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from nutella_fans.product.models import Product, Brand
from nutella_fans.save_substitute.models import Substitute
from django.contrib.auth import get_user_model
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from unittest import skip


options = webdriver.FirefoxOptions()
options.headless = True

class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        """Test on delete ans add favorite
        """
        self.driver = webdriver.Firefox(options=options)
        User = get_user_model()
        self.user = User.objects.create_user(
            username='Xavier', email='xavier@email.com', password='gabi@1428')
        b, created = Brand.objects.get_or_create(name='ferrero')
        brand_p1 = b.id

        p, created = Product.objects.get_or_create(name='Nutella - Ferrero - 1 kg',
                                                   nutriscore='e', nova=4,
                                                   url='https://fr.openfoodfacts.org/produit/'
                                                   '3017620425035/nutella-ferrero',
                                                   barcode=3017620425035,
                                                   description="Sucre, huile de palme, noisettes 13%"
                                                   " lait écrémé en poudre 8,7%"
                                                   "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                                   picture='https://images.openfoodfacts.org/images/'
                                                   ' products/301/762/042/2003/front_en.288.400.jpg',
                                                   brand_id=brand_p1)

        sb, created = Brand.objects.get_or_create(name='Funky Veggie')
        brand_p2 = sb.id
        self.product_id = p.id
        s, created = Product.objects.get_or_create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                   nutriscore='b', nova=3,
                                                   url='https://fr.openfoodfacts.org/produit/'
                                                   '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                   barcode=3770008009653,
                                                   description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                   "sucre de fleur de coco*, eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                   "ingrédients issus de l'agriculture biologique ",
                                                   brand_id=brand_p2)
        self.substitute_id = s.id

        self.favorite = Substitute.objects.create(
            product_id=self.product_id, substitute_id=self.substitute_id)
        self.favorite_id = self.favorite.id
        self.user.substitutes.add(self.favorite_id)

    @skip("Test on localhost OK --> Don't want to test for travis")
    def test_add_favorite_list(self):

        self.driver.implicitly_wait(20)
        self.driver.get('http://127.0.0.1:8000/account/login/')
        # self.driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        self.driver.find_element_by_id('id_username').send_keys('Xavier')
        self.driver.find_element_by_name('password').send_keys('gabi@1428')
        self.driver.find_element_by_class_name('account-btn').click()
        search_bar = self.driver.find_element_by_name("search_product")
        search_bar.send_keys("Nutella")
        search_bar.send_keys(Keys.RETURN)
        substitute = self.driver.find_elements_by_xpath(
            "//i[@class='bi bi-search']")[0]
        time.sleep(5)
        self.driver.implicitly_wait(5)
        substitute.click()
        favorite = self.driver.find_elements_by_xpath(
            "//button[@name='btn-favorate']")[0]
        time.sleep(5)
        self.driver.implicitly_wait(5)
        favorite.click()
        self.assertIn('Vos Favoris', self.driver.page_source)

    def test_favorite_delete(self):
        driver = self.driver
        driver.implicitly_wait(20)
        # driver.get('http://127.0.0.1:8000/account/login/')
        driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        driver.find_element_by_id('id_username').send_keys('Xavier')
        driver.find_element_by_name('password').send_keys('gabi@1428')
        driver.find_element_by_class_name('account-btn').click()
        driver.get('%s%s' % (self.live_server_url, '/favorites_list/'))
        # driver.get('http://127.0.0.1:8000/favorites_list/')
        delete = driver.find_elements_by_xpath(
            "//a[@name='delete_favorate']")[0]
        time.sleep(5)
        self.driver.implicitly_wait(5)
        delete.click()
        driver.find_element_by_name('Confirm_btn').click()
        self.assertIn('Vos Favoris', self.driver.page_source)
