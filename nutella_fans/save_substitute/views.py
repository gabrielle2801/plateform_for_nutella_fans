from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages


from nutella_fans.save_substitute.models import Substitute, Product
from nutella_fans.users_account.models import User


class FavorateList(ListView):

    """
    List of healthy product saved by user

    Attributes:
        context_object_name (str): my own name for object list return
        model (TYPE): Substitute Model imported
        template_name (str): location of template
    """

    template_name = 'favorites_list.html'
    model = Substitute
    context_object_name = 'favorite_list'

    def get_queryset(self):
        """Query according to user's login id

        Returns:
            TYPE: Description
        """

        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


def handle_server_error(request):
    return render(request, '500.html')

class SubtituteSaveView(LoginRequiredMixin, CreateView):

    """
    Saved healthy and unhealthy products on database if user is logged

    Attributes:
        fields (list): id of product and substitute
        on table save_substitute_substitute
        model (TYPE): Substitute Model
        template_name (str): location of template
    """

    template_name = 'substitute_list.html'
    model = Substitute
    fields = ['product', 'substitute']

    def post(self, request, *args, **kwargs):
        """
        create and save on database (Table save_substitute_substitute)

        Args:
            request (TYPE): message display
            *args: Description
            **kwargs: Description

        Returns:
            template : redirect to favorites template
        """

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


class FavoriteDeleteView(LoginRequiredMixin, DeleteView):

    """
    Delete favorite product of the list

    Attributes:
        model (TYPE): Substitute model
        success_url (TYPE): url of favorite template if is ok
    """

    model = Substitute
    context_object_name = 'favorite_list'
    template_name = 'substitute_confirm_delete.html'

    def get_queryset(self):
        """Query according to user's login id

        Returns:
            TYPE: Description
        """

        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)

    def get_success_url(self):
        messages.success(self.request, 'Le substitut a bien été supprimé')
        return reverse_lazy('favorites_list')
