from django.db import migrations, transaction


@transaction.atomic
def create_administrator_group(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    permission = apps.get_model('auth', 'Permission')

    add_user = permission.objects.get(codename='add_user')
    change_user = permission.objects.get(codename='change_user')
    delete_user = permission.objects.get(codename='delete_user')
    view_user = permission.objects.get(codename='view_user')

    administrators_permissions = [
        add_user,
        change_user,
        delete_user,
        view_user
    ]

    administrators, _ = group.objects.get_or_create(name='Administrators')
    for perm in administrators_permissions:
        administrators.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_users_permissions'),
    ]

    operations = [
        migrations.RunPython(create_administrator_group)
    ]
