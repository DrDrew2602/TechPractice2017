from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["discount", "created", "updated"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['user', 'petition', 'description']
