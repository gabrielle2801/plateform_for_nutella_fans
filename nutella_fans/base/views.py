from django.views import View
from django.shortcuts import render


def base(request):
    return render(request, 'base.html')


class BaseView(View):
    template_name = "templates/base.html"


def home(request):
    return render(request, 'home.html')


def mention(request):
    return render(request, 'legal_notice.html')
