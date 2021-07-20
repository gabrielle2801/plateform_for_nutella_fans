from django.urls import path

from nutella_fans.product.views import ProductListView, SubstituteListView

urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('substitute_list/', SubstituteListView.as_view(), name='substitute_list'),
]
