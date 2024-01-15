from django.core.management.base import BaseCommand
from nutella_fans.product.models import Product, Brand
from nutella_fans.save_substitute.models import Substitute
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.filter(username='Gabrielle').delete()
        User.objects.filter(username='Marcus').delete()
        u, created = User.objects.get_or_create(username="Gabrielle",
                                                email="gabrielle@email.com", password='12@test@12')
        self.stdout.write(self.style.SUCCESS("User Create"))
        b, created = Brand.objects.get_or_create(name='ferrero')
        brand_p1 = b.id

        p, created = Product.objects.get_or_create(name='Nutella - Ferrero - 400 g',
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
        self.stdout.write(self.style.SUCCESS("Product Create"))
        sb, created = Brand.objects.get_or_create(name='Lu')
        brand_p2 = sb.id
        self.product_id = p.id
        s, created = Product.objects.get_or_create(name='Prince Chocolat',
                                                   nutriscore='d', nova=4,
                                                   url='https://fr.openfoodfacts.org/produit/'
                                                   '7622210449283/prince-chocolat-lu',
                                                   barcode=7622210449283,
                                                   description="Céréales 50% (farine de blé 34.8%, farine de blé complète 15,7%),"
                                                   "sucre, huiles végétales (palme, colza), cacao maigre en poudre 4,5%, sirop de glucose,"
                                                   "amidon de blé, poudre à lever (carbonate d'ammonium, carbonate acide de sodium), "
                                                   "émulsifiant (lécithine de soja), sel, lait écrémé en poudre, perméat de lactosérum (de lait), arômes.",
                                                   picture='/images/products/762/221/044/9283/front_fr.437.200.jpg',
                                                   brand_id=brand_p2)
        self.substitute_id = s.id
        self.stdout.write(self.style.SUCCESS("Product Substitute Create"))
        self.substitute_id = Substitute.objects.create(
            product_id=self.product_id, substitute_id=self.substitute_id).pk
        u.substitutes.add(self.substitute_id)
        self.stdout.write(self.style.SUCCESS("Favorite Create"))
