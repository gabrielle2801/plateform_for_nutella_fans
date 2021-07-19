from django.urls import path
from nutella_fans.users_account import views
from nutella_fans.users_account.views import LoginView, SignupView
from django.conf.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.base, name='base'),
    path('', views.home, name='home'),
    path('sign_up/', SignupView.as_view(), name='sign_up'),
    path('logout/', views.logout_request, name='logout'),
]
