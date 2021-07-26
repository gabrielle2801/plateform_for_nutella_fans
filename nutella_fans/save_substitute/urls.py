from django.urls import path
# from django.contrib.auth.decorators import login_required

from nutella_fans.save_substitute.views import SubtituteSaveView

urlpatterns = [
    path('favorites_list/', SubtituteSaveView.as_view(),
         name='favorites_list'),
]
