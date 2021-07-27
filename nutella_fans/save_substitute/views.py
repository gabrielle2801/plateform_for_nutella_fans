from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from nutella_fans.save_substitute.models import Substitute, Product
from nutella_fans.users_account.models import User


class FavorateListView(ListView):
    template_name = 'favorites_list.html'
    model = Substitute
    context_object_name = 'favorite_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data()
        # Add in a QuerySet of all the substitutes
        context['favorite_list'] = Substitute.objects.filter(
            user=self.request.user)
        return context

    def get_queryset(self, *args, **kwargs):
        # product = self.request.GET.get('product_id')
        substitute = Substitute.objects.filter(
            substitute_id=self.request.GET.get('substitute_id'))

        return substitute


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
        return render(request, 'favorites_list.html')
