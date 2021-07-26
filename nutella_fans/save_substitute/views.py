from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render

from nutella_fans.save_substitute.models import Substitute
from nutella_fans.users_account.models import User
# from nutella_fans.save_substitute.forms import FavoriteCreateForm


class SubtituteSaveView(LoginRequiredMixin, CreateView):
    template_name = 'favorites_list.html'
    model = Substitute
    fields = '__all__'
    # form_class = FavoriteCreateForm
    success_url = reverse_lazy('favorites_list')

    def form_valid(self, form):
        self.object = form.save()
        object.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        # product_id = request.POST.get('product.id')
        product_id = self.kwargs.get('product.id')
        substitute_id = self.kwargs.get('substitute.id')
        return super().post(request, product_id=product_id, substitute_id=substitute_id)


class UserSaveFavoriteView(LoginRequiredMixin, CreateView):
    model = User
    fields = '__all__'

    def form_valid(self, form):
        form.instance.substitutes = self.request.user_login
        return super().form_valid(form)
