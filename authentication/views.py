from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import RegistrationForm, LoginForm


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('authentication:login')

    def form_valid(self, form: RegistrationForm):
        valid = super(RegisterView, self).form_valid(form)
        login(self.request, self.object)
        return valid

    def form_invalid(self, form: RegistrationForm):
        errors = form.errors.get_json_data()

        for msg in errors:
            messages.error(self.request, errors[msg][0]['message'])

        return super(RegisterView, self).form_invalid(form)


class LoginView(FormView):

    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('authentication:register')

    def form_valid(self, form: LoginForm):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form: LoginForm):
        errors = form.errors.get_json_data()

        for msg in errors:
            messages.error(self.request, errors[msg][0]['message'])

        return super(LoginView, self).form_invalid(form)


class LogoutView(LoginRequiredMixin, RedirectView):

    url = reverse_lazy('authentication:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
