# from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import RegistrationForm

# Create your views here.


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "register.html"
