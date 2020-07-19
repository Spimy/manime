import re
from difflib import SequenceMatcher as SM
from django import forms


def validate_password_strength(password, username):

    min_length = 8

    if (SM(None, password, username).ratio() * 100) >= 80:
        raise forms.ValidationError(
            'Password is too similar to username',
            code='bad'
        )

    if len(password) < min_length:
        raise forms.ValidationError(
            f'Password must be at least {min_length} characters long',
            code='invalid'
        )

    if not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9]){{{0},}}'.format(min_length), password):
        raise forms.ValidationError(
            'Password must contain both letters and digits',
            code='invalid'
        )

    if not any(c.isupper() for c in password):
        raise forms.ValidationError(
            'Password must contain at least 1 uppercase letter',
            code='invalid'
        )
