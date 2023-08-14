from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm, UserChangeForm
from .models import User, FoodItem
from django.utils.translation import gettext_lazy as _
from django.db import models

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name']

    



