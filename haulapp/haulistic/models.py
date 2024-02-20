from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import AbstractUser

User = get_user_model()

"""
    jak robisz custom usera bazowanego na tym z django to w admin.py i settings.py
    odkomentuj User'a i doimportuj ich z modeli i wywal 'User = get_user_model()'
"""
# class User(AbstractUser):
#     pfpurl = models.TextField(default='/static/pfp_default.png')


class Shopping_List(models.Model):
    list_name = models.CharField(max_length=32)
    list_category = models.CharField(max_length=32, blank=True)
    list_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # list_elements = models.CharField(max_length=254, blank=True)
    
    def __str__(self):
        return self.list_name


class List_Element(models.Model):
    list_pk = models.ForeignKey(Shopping_List, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=32)
    element_description = models.TextField(blank=True)
    amount = models.PositiveIntegerField(default=1)
    bought = models.BooleanField(default=0)


class To_Do_List(models.Model):
    list_name = models.CharField(max_length=32)
    list_category = models.CharField(max_length=32, blank=True)
    list_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.list_name


class To_Do_Element(models.Model):
    list_pk = models.ForeignKey(To_Do_List, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=32)
    element_description = models.TextField(blank=True)
    completed = models.BooleanField(default=0)

