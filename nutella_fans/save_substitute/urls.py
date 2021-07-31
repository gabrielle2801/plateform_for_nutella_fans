from django.urls import path
# from django.contrib.auth.decorators import login_required

from nutella_fans.save_substitute.views import FavorateListView, SubtituteSaveView, FavoriteDeleteView

urlpatterns = [
    path('substitute_save/', SubtituteSaveView.as_view(), name='substitute_save'),
    path('favorites_list/', FavorateListView.as_view(), name='favorites_list'),
    path('delete_favoris/<int:pk>',
         FavoriteDeleteView.as_view(), name='delete_favoris'),
]
