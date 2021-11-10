from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from nutella_fans.save_substitute.models import Substitute
from nutella_fans.product.models import Product, Brand

options = webdriver.FirefoxOptions()
# options.headless = True
class PurBeurreTest(StaticLiveServerTestCase):

    def setUp(self):
        """Summary
        """
        self.driver = webdriver.Firefox(options=options)

        self.brand_p1 = Brand.objects.create(name='ferrero').pk
        self.brand_p2 = Brand.objects.create(name='LU').pk
        self.product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                              nutriscore='e', nova=4,
                                              url='https://fr.openfoodfacts.org/produit/'
                                              '3017620422003/nutella-ferrero',
                                              barcode=3017620422003,
                                              description="Sucre, huile de palme, noisettes 13%"
                                              " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=self.brand_p1).pk
        self.product_better = Product.objects.create(name='Prince Chocolat',
                                                     nutriscore='d', nova=4,
                                                     url='https://fr.openfoodfacts.org/produit/'
                                                     '7622210449283/prince-chocolat-lu',
                                                     barcode=7622210449283,
                                                     description="Céréales 50% (farine de blé 34.8%, farine de blé complète 15,7%),"
                                                     "sucre, huiles végétales (palme, colza), cacao maigre en poudre 4,5%, sirop de glucose,"
                                                     "amidon de blé, poudre à lever (carbonate d'ammonium, carbonate acide de sodium), "
                                                     "émulsifiant (lécithine de soja), sel, lait écrémé en poudre, perméat de lactosérum (de lait), arômes.",
                                                     picture='/images/products/762/221/044/9283/front_fr.437.200.jpg',
                                                     brand_id=self.brand_p2).pk

        self.product_favorate = Substitute.objects.create(
            product_id=self.product, substitute_id=self.product_better).pk
        self.user.substitutes.add(self.product_favorate)
        return super(PurBeurreTest, self).setUp()

    def test_create_user(self):
        self.driver.get('http://127.0.0.1:8000/account/login/')
        # driver.implicitly_wait(20)
        # driver.get('%s%s' % (self.live_server_url, '/account/login/'))
        User = get_user_model()
        user = User.objects.create_user(
            username="Gabrielle",
            email="gabrielle@email.com",
        )
        user.set_password("xavier@1428")
        user.save()
        self.driver.find_element_by_id('id_username').send_keys('Gabrielle')
        self.driver.find_element_by_name('password').send_keys('xavier@1428')
        self.driver.find_element_by_class_name('account-btn').click()


'''
    def test_add_favorite_list(self):
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
'''
