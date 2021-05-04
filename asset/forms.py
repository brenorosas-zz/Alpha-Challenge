from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from .models import *


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length = 255, required = True, label = 'First Name')
    last_name = forms.CharField(max_length = 255, required = True, label = 'Last Name')
    class Meta:
        model = User
        fields = ("first_name", "last_name","username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class AssetForm(forms.ModelForm):
    update_time = models.IntegerField(default = 60)
    inferior_limit = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    upper_limit = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    class Meta:
        model = Asset
        fields = ['update_time', 'inferior_limit', 'upper_limit',]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('inferior_limit') < 0 or cleaned_data.get('upper_limit') < 0 or cleaned_data.get('update_time') < 0:
            raise  ValidationError("The values can not be negative")
        if cleaned_data.get('inferior_limit') > cleaned_data.get('upper_limit'):
            raise  ValidationError("The upper limit can not be lower than the inferior limit")  
        return cleaned_data

    def save(self, commit = True, *args, **kwargs):
        self.cleaned_data = self.clean()
        asset = Asset(
            name = kwargs['ticker'],
            user = User.objects.get(id = kwargs['id']),
            update_time = self.cleaned_data['update_time'],
            upper_limit = self.cleaned_data['upper_limit'],
            inferior_limit = self.cleaned_data['inferior_limit'],
        )
        if commit:
            asset.save()
        return asset