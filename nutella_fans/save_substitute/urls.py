from django.urls import path


from nutella_fans.save_substitute.views import FavorateList, SubtituteSaveView, FavoriteDeleteView

urlpatterns = [
    path('substitute_save/', SubtituteSaveView.as_view(), name='substitute_save'),
    path('favorites_list/', FavorateList.as_view(), name='favorites_list'),
    path('delete_favorate/<int:fav>',
         FavoriteDeleteView.as_view(), name='delete_favorate'),
]
handler500 = "nutella_fans.save_substitute.views.handle_server_error"
