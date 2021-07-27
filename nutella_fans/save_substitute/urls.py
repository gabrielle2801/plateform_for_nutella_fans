from django.urls import path
# from django.contrib.auth.decorators import login_required

from nutella_fans.save_substitute.views import FavorateListView, SubtituteSaveView

urlpatterns = [
    path('substitutes/', SubtituteSaveView.as_view(), name='substitute_list'),
    path('favorites_list/', FavorateListView.as_view(), name='favorites_list'),
]
