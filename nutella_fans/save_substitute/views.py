from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


from nutella_fans.save_substitute.models import Substitute, Product
from nutella_fans.users_account.models import User


class FavorateListView(ListView):
    template_name = 'favorites_list.html'
    model = Substitute
    context_object_name = 'favorite_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SubtituteSaveView(LoginRequiredMixin, CreateView):
    template_name = 'substitute_list.html'
    model = Substitute
    fields = ['product', 'substitute']

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(
            pk=self.request.POST.get('product_id'))
        substitute = Substitute.objects.filter(
            product_id=product.id, substitute_id=self.request.POST.get('substitute_id'))
        user_id = request.user
        user = User.objects.get(id=user_id.id)
        if not substitute.exists():
            substitute = Substitute.objects.create(product_id=product.id,
                                                   substitute_id=self.request.POST.get('substitute_id'))

            user.substitutes.add(substitute)
            messages.success(
                request, 'Le produit est bien dans votre liste de favoris')
        else:
            messages.warning(
                request, 'Le produit existe déja dans votre liste de favoris')
        return redirect('favorites_list')


class FavoriteDeleteView(DeleteView):
    model = Substitute
    success_url = reverse_lazy('favorites_list')

    def get(self, request, *args, **kwargs):
        substitute_id = self.kwargs.get('fav.id')
        delete = self.post(request, Substitute.objects.filter(
            substitute_id=substitute_id).delete())
        messages.success(request, 'Le substitut a bien été supprimé')
        return delete
