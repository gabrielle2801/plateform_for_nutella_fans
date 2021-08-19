from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
# from django.shortcuts import get_object_or_404

from nutella_fans.users_account.forms import UserCreationForm
from nutella_fans.users_account.models import User


class SignupView(View):
    form_class = UserCreationForm
    template_name = "registration/sign_up.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
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
    template_name = "registration/login.html"


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('base')


class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
