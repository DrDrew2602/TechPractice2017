from django import forms
from django.contrib.auth.admin import UserCreationForm
from .models import *


class CheckoutContactForm(UserCreationForm):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField()