"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from CatDatabase.models import Cat
from app import models
from django.contrib.auth.forms import UserCreationForm

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['Name', 'Breed', 'Age', 'Gender', 'Description']

class AccountCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('medical_staff', 'Medical Staff'),
            ('caretaker', 'Caretaker')
        ],
        required=True
    )

    class Meta:
        model = models.Account
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'role']