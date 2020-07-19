from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    # UserChangeForm,
    # PasswordChangeForm
)
from django.contrib.auth import get_user_model
from .utils import validate_password_strength

User = get_user_model()


class RegistrationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': '\uf007'})
    )

    email = forms.EmailField(required=True, label='Email', max_length=255,
                             widget=forms.EmailInput(
                                 attrs={'placeholder': '\uf0e0'})
                             )

    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': '\uf023'})
                                )

    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': '\uf023'})
                                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ''

        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'An account has already been registered with given username',
                code='unique'
            )

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account has already been registered with given email',
                code='unique'
            )

        password1 = cleaned_data.get('password1')
        validate_password_strength(password1, username)

        return cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):

    error_messages = {
        'invalid_login': ('The username or password you have entered is invalid.'),
        'inactive': ('This account is inactive.'),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    username = forms.CharField(label='Email or Username',
                               widget=forms.widgets.TextInput(
                                   attrs={'placeholder': "\uf007"})
                               )

    password = forms.CharField(label='Password',
                               widget=forms.widgets.PasswordInput(
                                   attrs={'placeholder': "\uf023"})
                               )
