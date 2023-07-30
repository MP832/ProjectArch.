from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.validators import RegexValidator
from django.forms import ModelForm,widgets

domain_validator = RegexValidator(
    regex='@(gmail.com)$',
    message='Domain not valid',
    code='invalid_domain',
)

class ContactForm(ModelForm):
    class Meta:
        model = Bezoeker
        fields = ['fname','lname','functie','email','evenements']


class aanwezig(ModelForm):
    class Meta:
        model = Bezoeker
        fields = ('aanwezigheid',)

    