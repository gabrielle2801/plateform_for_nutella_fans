from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render

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
        product = Product.objects.get(pk=self.kwargs.get('product_id'))
        context['product'] = product
        return context

    def get_queryset(self, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        return product.get_substitutes()


class ProductDetailView(DetailView):
    template_name = 'product/detail_substitute.html'
    model = Product
