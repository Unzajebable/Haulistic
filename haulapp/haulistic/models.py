from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pfpurl = models.TextField(default='/static/pfp_default.png')


@receiver(post_save, sender=User)
def create_default_lists(sender, created, instance, **kwargs):
    if created:
        Shopping_List.objects.create(list_name="Default Shopping List", list_owner=instance)
        To_Do_List.objects.create(list_name="Default To Do List", list_owner=instance)


class Shopping_List(models.Model):
    list_name = models.CharField(max_length=32)
    list_category = models.CharField(max_length=32, blank=True)
    list_owner = models.ForeignKey(User, on_delete=models.CASCADE)


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



class To_Do_Element(models.Model):
    list_pk = models.ForeignKey(To_Do_List, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=32)
    element_description = models.TextField(blank=True)
    completed = models.BooleanField(default=0)

