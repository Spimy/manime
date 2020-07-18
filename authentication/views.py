# from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls.base import reverse
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = 'register.html'

    def form_invalid(self, form: RegistrationForm):

        errors = form.errors.get_json_data()
        error_msg = errors['__all__'][0]['message']
        messages.error(self.request, error_msg)

        return super(RegisterView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('authentication:register')
