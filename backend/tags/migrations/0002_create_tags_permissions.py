from django.contrib.auth.management import create_permissions
from django.db import migrations, transaction


@transaction.atomic
def create_tags_permissions(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_tags_permissions)
    ]
