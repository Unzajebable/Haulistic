from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

from .models import Shopping_List, List_Element, To_Do_List, To_Do_Element


User = get_user_model()


class AddUserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password2', 'email']
        widgets = {
            "password": forms.PasswordInput,
            'email': forms.EmailInput,
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password': 'Password',
            'email': 'E-mail address',
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
        labels = {
            'username': 'Username',
            'password': 'Password'
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


class AddShoppingListForm(forms.ModelForm):
    class Meta:
        model = Shopping_List
        fields = ['list_name', 'list_category']     # dodać pk list ownera jako hidden input
        labels = {
            'list_name': 'Name of the shopping list',
            'list_category': 'Category of the shopping list (not required)'
        }


class AddShoppingListElementForm(forms.ModelForm):
    class Meta:
        model = List_Element
        fields = ['element_name', 'element_description', 'amount', 'list_pk']
        widgets = {'list_pk': forms.HiddenInput}
        labels = {
            'element_name': 'Name of the product',
            'element_description': 'Product description, color, link or w/e you desire (not required)',
            'amount': 'Amount of products to buy'
        }


class AddToDoListForm(forms.ModelForm):
    class Meta:
        model = To_Do_List
        fields = ['list_name', 'list_category']     # dodać pk list ownera jako hidden input
        labels = {
            'list_name': 'Name of the To-Do list',
            'list_category': 'Category of the to do list (not required)'
        }


class AddToDoElementForm(forms.ModelForm):
    class Meta:
        model = To_Do_Element
        fields = ['element_name', 'element_description', 'list_pk']
        widgets = {'list_pk': forms.HiddenInput}
        labels = {
            'element_name': 'Name of the task',
            'element_description': 'Task description (not required)'
        }