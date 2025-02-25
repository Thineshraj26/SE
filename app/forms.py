"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from CatDatabase.models import Cat, Appointment, Treatment
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
        fields = ['first_name', 'last_name', 'username','email', 'password1', 'password2', 'role']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Date', 'Time', 'Reason']
        widgets = {
            'Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'Reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ["StartDate", "EndDate", "TreatmentName", "Description"]
        labels = {
            "StartDate": "Start Date",
            "EndDate": "End Date",
            "TreatmentName": "Medication",
            "Description": "Details"
        }
        widgets = {
            "StartDate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "EndDate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "TreatmentName": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter medication name"}),
            "Description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter treatment details"})
        }