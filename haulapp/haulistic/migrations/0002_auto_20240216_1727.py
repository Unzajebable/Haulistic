from django.db import migrations
from haulistic.models import Shopping_List


class Migration(migrations.Migration):
    
    def create_default_list(apps, schema_editor):
        Shopping_List.objects.create(list_name="Default", list_owner=1)
    
    dependencies = [
        ('haulistic', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_list)
    ]
