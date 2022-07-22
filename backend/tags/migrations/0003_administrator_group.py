from django.apps import apps as global_apps
from django.db import migrations, transaction


@transaction.atomic
def administrator_group_permissions(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    permission = apps.get_model('auth', 'Permission')

    add_tags = permission.objects.get(codename='add_tags')
    change_tags = permission.objects.get(codename='change_tags')
    delete_tags = permission.objects.get(codename='delete_tags')
    view_tags = permission.objects.get(codename='view_tags')

    administrators_permissions = [
        add_tags,
        change_tags,
        delete_tags,
        view_tags
    ]

    if group.objects.filter(name='Administrators').exists():
        administrators = group.objects.get(name='Administrators')
        for perm in administrators_permissions:
            administrators.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_create_tags_permissions'),
    ]

    operations = [
        migrations.RunPython(administrator_group_permissions)
    ]

    if global_apps.is_installed('users'):
        dependencies.append(('users', '0003_administrator_group'))
