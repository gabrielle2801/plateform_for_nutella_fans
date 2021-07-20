from django.views.generic import ListView

from nutella_fans.product.models import Product


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product

    def get_queryset(self):
        search = self.request.GET.get('search_product', '').strip()
        qs = super().get_queryset()
        if search:

            return qs.filter(name__icontains=search)
        else:
            return qs


class SubstituteListView(ListView):
    template_name = 'substitute_list.html'
    model = Product

    def get_queryset(self, barcode):
        search_substitute = self.request.GET.get('search_substitute')
        qs = super().get_queryset()
        if search_substitute:
            product = Product.objects.get(barcode=barcode)
            product_categories = product.categories.all()

            return Product.objects.filter(categories__in=product_categories)\
                .filter(nutriscore__lt=product.nutriscore)\
                .order_by('nutriscore').distinct()
        else:
            return qs
