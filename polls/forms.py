from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    tailwind_class = "w-full border-2 border-gray-300 bg-gray-100 rounded-lg focus:ring focus:border-blue-300 focus:shadow-none"

    username = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class}),
                                error_messages={
                                'unique': 'This username is already in use.',
                                'invalid': 'Invalid username format.',
                                'max_length': 'Username should not exceed 150 characters.',
                            }
                        )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}),
                                error_messages={'min_length': 'Password must contain at least 8 characters.',}
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}),)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }