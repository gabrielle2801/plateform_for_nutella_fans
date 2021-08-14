from django.urls import path

from nutella_fans.product.views import ProductListView, SubstituteListView, ProductDetailView

urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('substitutes/<int:product_id>',
         SubstituteListView.as_view(), name='substitute_list'),
    path('detail_substitute/<int:pk>',
         ProductDetailView.as_view(), name='detail_substitute'),
]
