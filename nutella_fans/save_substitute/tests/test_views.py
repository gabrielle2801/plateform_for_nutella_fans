from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User


from nutella_fans.product.models import Product, Brand
from nutella_fans.save_substitute.models import Substitute
from nutella_fans.save_substitute.views import FavorateList, SubtituteSaveView, FavoriteDeleteView
from nutella_fans.users_account.models import User


class FavoriteListTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        brand_p1 = Brand.objects.create(name='ferrero').pk
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                              nutriscore='e', nova=4,
                                              url='https://fr.openfoodfacts.org/produit/'
                                              '3017620422003/nutella-ferrero',
                                              barcode=3017620422003,
                                              description="Sucre, huile de palme, noisettes 13%"
                                              " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=brand_p1)
        product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                nutriscore='b', nova=3,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                barcode=3770008009653,
                                                description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                "sucre de fleur de coco*,"
                                                "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                "ingrédients issus de l'agriculture biologique",
                                                picture='https://images.openfoodfacts.org/images/'
                                                ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                brand_id=brand_p2)

        product_id = product.pk
        substitute_id = product_better.pk
        self.favorite = Substitute.objects.create(
            product_id=product_id, substitute_id=substitute_id)
        self.user = User.objects.create_user(
            username='user', email='user@email.com', password='12test12')
        return super().setUp()

    def test_favorite_with_valid_user(self):
        request = self.factory.get('favorites_list')
        request.user = self.user
        response = FavorateList.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_favorite_list(self):
        login = self.client.login(username='user', password='12test12')
        self.assertTrue(login)
        favorite_url = reverse('favorites_list')
        response = self.client.get(favorite_url)
        self.assertEquals(response.status_code, 200)

class SaveFavoriteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@email.com', password='12test12')

    def test_favorite_saved(self):
        brand_p1 = Brand.objects.create(name='ferrero').pk
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                              nutriscore='e', nova=4,
                                              url='https://fr.openfoodfacts.org/produit/'
                                              '3017620422003/nutella-ferrero',
                                              barcode=3017620422003,
                                              description="Sucre, huile de palme, noisettes 13%"
                                              " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=brand_p1)
        product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                nutriscore='b', nova=3,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                barcode=3770008009653,
                                                description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                "sucre de fleur de coco*,"
                                                "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                "ingrédients issus de l'agriculture biologique",
                                                picture='https://images.openfoodfacts.org/images/'
                                                ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                brand_id=brand_p2)

        login = self.client.login(username='user', password='12test12')
        self.assertTrue(login)
        response = self.client.post(reverse('substitute_save'), {
            'product_id': product.id, 'substitute_id': product_better.id}, follow=True)
        self.assertEquals(response.status_code, 200)


class DeleteFavoriteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@email.com', password='12test12')
        self.other_user = User.objects.create_user(
            username='other', email='other@email.com', password='12other12')

    def test_favorite_delete_logged(self):
        brand_p1 = Brand.objects.create(name='ferrero').pk
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                         nutriscore='e', nova=4,
                                         url='https://fr.openfoodfacts.org/produit/'
                                         '3017620422003/nutella-ferrero',
                                         barcode=3017620422003,
                                         description="Sucre, huile de palme, noisettes 13%"
                                         " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=brand_p1).pk
        product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                nutriscore='b', nova=3,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                barcode=3770008009653,
                                                description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                "sucre de fleur de coco*,"
                                                "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                "ingrédients issus de l'agriculture biologique",
                                                picture='https://images.openfoodfacts.org/images/'
                                                ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                brand_id=brand_p2).pk

        login = self.client.login(username='user', password='12test12')
        self.assertTrue(login)
        response = self.client.post(reverse('substitute_save'), {
            'product_id': product, 'substitute_id': product_better}, follow=True)
        product_favorate = Substitute.objects.create(
            product_id=product, substitute_id=product_better).pk
        self.user.substitutes.add(product_favorate)

        self.assertEquals(response.status_code, 200)
        delete_url = reverse('delete_favorate', kwargs={
                             'pk': product_favorate})

        response = self.client.post(delete_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/favorites_list/')

    def test_favorite_delete_unlogged(self):
        response = self.client.post('delete_favorate/19')
        self.assertEquals(response.status_code, 404)

    def test_favorite_other_user(self):
        brand_p1 = Brand.objects.create(name='ferrero').pk
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                         nutriscore='e', nova=4,
                                         url='https://fr.openfoodfacts.org/produit/'
                                         '3017620422003/nutella-ferrero',
                                         barcode=3017620422003,
                                         description="Sucre, huile de palme, noisettes 13%"
                                         " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=brand_p1).pk
        product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                nutriscore='b', nova=3,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                barcode=3770008009653,
                                                description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                "sucre de fleur de coco*,"
                                                "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                "ingrédients issus de l'agriculture biologique",
                                                picture='https://images.openfoodfacts.org/images/'
                                                ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                brand_id=brand_p2).pk

        response = self.client.post(reverse('substitute_save'), {
            'product_id': product, 'substitute_id': product_better}, follow=True)
        product_favorate = Substitute.objects.create(
            product_id=product, substitute_id=product_better).pk
        self.user.substitutes.add(product_favorate)
        login = self.client.login(username='other', password='12other12')
        self.assertTrue(login)
        delete_url = reverse('delete_favorate', kwargs={
                             'pk': product_favorate})
        response = self.client.post(delete_url)
        self.assertEquals(response.status_code, 404)
