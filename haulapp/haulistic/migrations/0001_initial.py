from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List_Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_pk', models.PositiveIntegerField(default=0)),
                ('element_name', models.CharField(max_length=32)),
                ('element_description', models.TextField(blank=True)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('bought', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shopping_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=32)),
                ('list_category', models.CharField(blank=True, max_length=32)),
                ('list_elements', models.CharField(blank=True, max_length=254)),
            ],
        ),
    ]
