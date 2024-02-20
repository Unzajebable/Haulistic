# Generated by Django 5.0.2 on 2024-02-17 16:36

from django.db import migrations
from haulistic.models import To_Do_List


class Migration(migrations.Migration):

    def create_default_to_do(apps, schema_editor):
        To_Do_List.objects.create(list_name="Default", list_owner=1)
    
    dependencies = [
        ('haulistic', '0003_to_do_element_to_do_list_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_to_do)
    ]