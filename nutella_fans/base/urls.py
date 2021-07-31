from django.urls import path

from nutella_fans.base import views
# from nutella_fans.base.views import MentionView

urlpatterns = [
    path('', views.base, name='base'),
    path('', views.home, name='home'),
    path('legal_notice/', views.mention, name='legal_notice'),
]
