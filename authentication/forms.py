import re
from difflib import SequenceMatcher as SM

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm
)
from django.contrib.auth.models import User


def validate_password_strength(value):

    min_length = 8

    if len(value) < min_length:
        raise forms.ValidationError(
            f"Password must be at least {min_length} characters long")

    if (not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9]){{{0},}}".format(min_length), value)):
        raise forms.ValidationError(
            "Password must contain both letters and digits")

    # check for uppercase letter
    if not any(c.isupper() for c in value):
        raise forms.ValidationError(
            "Password must contain at least 1 uppercase letter")

    return value


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""

        for field_name in ["username", "email", "password1", "password2"]:
            self.fields[field_name].help_text = None

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "\uf007"}))
    email = forms.EmailField(required=True, label="Email", max_length=255,
                             widget=forms.EmailInput(attrs={
                                 "autofocus": True,
                                 "placeholder": "\uf0e0"
                             })
                             )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "\uf023"}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(
        attrs={"placeholder": "\uf023"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        return username

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account has already been registered with given email")
        return email

    def clean_password1(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")

        if username is None:
            return password1

        if (SM(None, password1, username).ratio() * 100) >= 80:
            print("password test")
            raise forms.ValidationError("Password is too similar to username")

        return validate_password_strength(password1)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
