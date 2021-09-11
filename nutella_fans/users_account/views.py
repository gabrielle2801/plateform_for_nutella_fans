"""Summary
"""
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView


from nutella_fans.users_account.forms import UserCreationForm
from nutella_fans.users_account.models import User


class SignupView(View):

    """Summary

    Attributes:
        form_class (TYPE): Description
        template_name (str): Description
    """

    form_class = UserCreationForm
    template_name = "registration/sign_up.html"

    def get(self, request, *args, **kwargs):
        """Summary

        Args:
            request (TYPE): HTTpRequest request to generate a answer
            *args: Description
            **kwargs: Description

        Returns:
            TYPE: HttpResponse object with template name and form information
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Form to login for user's account
        save users's information on database if form is valid
        on Class Based View
        class SignUpView(CreateView):
            form_class = UserCreationForm
            success_url = reverse_lazy('base')
            template_name = 'registration/sign_up.html'

        Args:
            request (TYPE): HTTpRequest request to generate a answer
            *args: Description
            **kwargs: Description

        Returns:
            TYPE: HttpResponse object with template name and form information
        """
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
        return render(request, self.template_name, {'form': form})


class LoginView(View):

    """Clas Based View for user's login

    Attributes:
        template_name (str): template location
    """

    template_name = "registration/login.html"


def logout_request(request):
    """ function to logout

    Args:
        request (TYPE): HTTpRequest request to generate a answer

    Returns:
        TYPE: redirect to base.html
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('base')


class UserDetailView(DetailView):

    """Class Based View for profile template

    Attributes:
        model (TYPE): User model imported
        template_name (str): Profile location template
    """

    model = User
    template_name = 'registration/profile.html'
