from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# class User(models.Model):
#     username = models.CharField(max_length=32)
#     user_facing_name = models.CharField(max_length=64)
#     password = models.CharField(max_length=100)
#     user_email = models.EmailField(max_length=200)


class Shopping_List(models.Model):
    list_name = models.CharField(max_length=32)
    list_category = models.CharField(max_length=32, blank=True)
    list_elements = models.CharField(max_length=254, blank=True)


class List_Element(models.Model):
    list_pk = models.PositiveIntegerField(default=0)
    element_name = models.CharField(max_length=32)
    element_description = models.TextField(blank=True)
    amount = models.PositiveIntegerField(default=1)
    bought = models.BooleanField(default=0)

