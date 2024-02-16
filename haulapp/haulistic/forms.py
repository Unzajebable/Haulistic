from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

from .models import Shopping_List, List_Element


User = get_user_model()


class AddUserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password2', 'email']
        widgets = {
            "password": forms.PasswordInput,
            'email': forms.EmailInput,
        }

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('password')
        pass2 = cd.get('password2')

        if pass2 != pass1:
            raise ValidationError("Passwords are mismached")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Password and/or login is incorrect")
        else:
            self.user = user


class AddListForm(forms.ModelForm):
    class Meta:
        model = Shopping_List
        fields = ['list_name', 'list_category']


class AddListElementForm(forms.ModelForm):
    class Meta:
        model = List_Element
        fields = ['element_name', 'element_description', 'amount', 'list_pk']
        widgets = {'list_pk': forms.HiddenInput}