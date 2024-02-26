from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User, Shopping_List, List_Element, To_Do_List, To_Do_Element


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'pfpurl']
        widgets = {
            "password": forms.PasswordInput,
            'email': forms.EmailInput,
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
            'email': 'E-mail address',
            'pfpurl': 'URL to your profile picture'
        }


# class EditUserForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = []


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Password and/or login is incorrect")
        else:
            self.user = user


class AddShoppingListForm(forms.ModelForm):
    class Meta:
        model = Shopping_List
        fields = ['list_name', 'list_category']     # dodać pk list ownera jako hidden input
        # widgets = {'list_owner': forms.HiddenInput}
        labels = {
            'list_name': 'Name of the shopping list',
            'list_category': 'Category of the shopping list (not required)'
        }


class AddShoppingListElementForm(forms.ModelForm):
    class Meta:
        model = List_Element
        fields = ['element_name', 'element_description', 'amount']
        # widgets = {'list_pk': forms.HiddenInput}
        labels = {
            'element_name': 'Name of the product',
            'element_description': 'Product description, color, link or w/e you desire (not required)',
            'amount': 'Amount of products to buy'
        }


class AddToDoListForm(forms.ModelForm):
    class Meta:
        model = To_Do_List
        fields = ['list_name', 'list_category']
        # widgets = {'list_owner': forms.HiddenInput}
        labels = {
            'list_name': 'Name of the To-Do list',
            'list_category': 'Category of the to do list (not required)'
        }


class AddToDoElementForm(forms.ModelForm):
    class Meta:
        model = To_Do_Element
        fields = ['element_name', 'element_description']
        # widgets = {'list_pk': forms.HiddenInput}
        labels = {
            'element_name': 'Name of the task',
            'element_description': 'Task description (not required)'
        }