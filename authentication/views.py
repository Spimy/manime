# from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.contrib import messages, auth
from .forms import RegistrationForm, LoginForm

# Create your views here.


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'auth.html'
    success_url = reverse_lazy('authentication:login')

    def form_invalid(self, form: RegistrationForm):
        errors = form.errors.get_json_data()
        messages.error(self.request, errors['__all__'][0]['message'])
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_type'] = ['Register', 'Sign up', 'Register']
        return context


class LoginView(FormView):

    form_class = LoginForm
    template_name = 'auth.html'
    success_url = reverse_lazy('authentication:register')

    def form_valid(self, form: LoginForm):
        auth.login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form: LoginForm):
        errors = form.errors.get_json_data()
        messages.error(self.request, errors['__all__'][0]['message'])
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_type'] = ['Login', 'Sign In', 'Authenticate']
        return context


class LogoutView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('next', '/')
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
