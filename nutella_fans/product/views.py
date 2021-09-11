from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from nutella_fans.product.models import Product


class ProductListView(ListView):

    """Class Based View list of product

    Attributes:
        model (Model class): Product Model imported
        template_name (str): template location
    """

    template_name = 'product_list.html'
    model = Product

    def get_queryset(self):
        """ List of products according to user's research
        queryset --> get products filter by 'search_product' from base.html form

        Returns:
            Dict: list of products model queryset
        """
        search = self.request.GET.get('search_product', '').strip()
        qs = super().get_queryset()
        if search:

            return qs.filter(name__icontains=search)
        else:
            return qs


class SubstituteListView(ListView):

    """Class Based View get better products by nustriscore


    Attributes:
        context_object_name (str): my own name for products list
        model (model class): Model Product impoted
        template_name (str): location of template
    """

    template_name = 'product/substitute_list.html'
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self):
        """
        We need to get more information about unhealthy product like the id
        for the queryset function

        Returns:
            DICT: ID of unhealthy product choice by user
        """
        context = super().get_context_data()
        product = Product.objects.get(pk=self.kwargs.get('product_id'))
        context['product'] = product
        return context

    def get_queryset(self, *args, **kwargs):
        """List of healthy products called substitutes
        Called get_substitutes function to sort subtitutes by nustriscore

        Args:
            *args: Description
            **kwargs: get args from template url variable

        Returns:
            INT: ID of product from url
        """
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)
        return product.get_substitutes()


class ProductDetailView(DetailView):

    """ Detail of product with not good nustriscore
        and substitutes (product with good nutriscore )
        sort by Fat, saturated_fat, saltn sugar
        and OpenFoodFacts url link

    Attributes:
        model (Model Class): Product model
        template_name (str): location of template
    """

    template_name = 'product/detail_product.html'
    model = Product
