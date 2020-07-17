from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class RegisterView(TemplateView):
    template_name = 'register.html'
    