# Generated by Django 5.0.2 on 2024-02-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haulistic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_element',
            name='element_name',
            field=models.CharField(max_length=132),
        ),
        migrations.AlterField(
            model_name='shopping_list',
            name='list_category',
            field=models.CharField(blank=True, max_length=132),
        ),
        migrations.AlterField(
            model_name='shopping_list',
            name='list_name',
            field=models.CharField(max_length=132),
        ),
        migrations.AlterField(
            model_name='to_do_element',
            name='element_name',
            field=models.CharField(max_length=132),
        ),
        migrations.AlterField(
            model_name='to_do_list',
            name='list_category',
            field=models.CharField(blank=True, max_length=132),
        ),
        migrations.AlterField(
            model_name='to_do_list',
            name='list_name',
            field=models.CharField(max_length=132),
        ),
    ]
