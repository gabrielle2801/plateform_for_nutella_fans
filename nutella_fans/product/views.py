from django.views.generic import ListView, DetailView

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
    template_name = 'product/substitute_list.html'
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self):
        context = super().get_context_data()
        context['product_id'] = self.kwargs.get('product_id')
        return context

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        product_categories = product.categories.all()
        result = Product.objects.filter(categories__in=product_categories)\
            .filter(nutriscore__lt=product.nutriscore)\
            .order_by('nutriscore').distinct()
        return result


class ProductDetailView(DetailView):
    template_name = 'product/detail_substitute.html'
    model = Product

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        substitute_id = self.kwargs.get('substitute_id')
        queryset = queryset.filter(pk=substitute_id)
        obj = queryset.get()
        # product_categories = product.categories.all()
        return obj
