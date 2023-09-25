import logging
from typing import Any

from django import forms
# from django.apps import apps
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question


class SignUpForm(UserCreationForm):
    tailwind_class = """w-full border-2 border-gray-300 bg-gray-100 rounded-lg
                        focus:ring focus:border-blue-300 focus:shadow-none"""
    logger = logging.getLogger('signup_form')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class}), error_messages={
                            'unique': 'This username is already in use.',
                            'invalid': 'Invalid username format.',
                            'max_length': 'Username should not exceed 150 characters.',
                            }
                        )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}),
                                error_messages={'min_length': 'Password must contain at least 8 characters.', }
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': tailwind_class}),)

    # commit -> default =True -> If commit is True -> want to save the user object to the database.
    def save(self, commit: bool = True) -> Any:
        user = super().save(commit=False)

        if commit:
            user.save()
            self.logger.info(f"User registered with username: {user.username}")

        return user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }


class PollSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PollCreateForm(forms.ModelForm):
    box_style = """w-full py-2 px-2 border-2 border-gray-300 bg-gray-100 rounded-lg
                focus:ring focus:border-blue-300 focus:shadow-none"""
    large_box_style = """w-full border-2 border-gray-300 bg-gray-100 rounded-lg
                        focus:ring focus:border-blue-300 focus:shadow-none"""

    question_text = forms.CharField(min_length=10, max_length=100, required=True,
                                    widget=forms.TextInput(attrs={'class': box_style,
                                                                  'placeholder': "What is your question?"}))
    pub_date = forms.DateTimeField(initial=timezone.now, required=True,
                                   widget=forms.DateInput(attrs={'type': 'date',
                                                                 'min': str(timezone.now()).split()[0]}))
    end_date = forms.DateTimeField(initial=timezone.now()+timezone.timedelta(1),
                                   widget=forms.DateInput(attrs={'type': 'date',
                                                          'min': str(timezone.now()+timezone.timedelta(1)).split()[0]}))
    short_description = forms.CharField(max_length=200,
                                        widget=forms.TextInput(
                                            attrs={'class': box_style,
                                                   'placeholder': "Short description (Maximum 200 characters)"}))
    long_description = forms.CharField(max_length=2000,
                                       widget=forms.Textarea(
                                            attrs={'class': large_box_style,
                                                   'placeholder': "Long description (Maximum 2000 characters)"}))
    user_choice = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter a choice'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tag = apps.get_model('polls', 'Tag')

        # tags = forms.MultipleChoiceField(
        #     choices=[(tag.id, tag.tag_text + "1131") for tag in Tag.objects.all()],
        #     widget=forms.CheckboxSelectMultiple,
        # )

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'end_date', 'short_description', 'long_description', 'tags']
