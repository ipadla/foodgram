from django.apps import apps as global_apps
from django.db import migrations, transaction


@transaction.atomic
def administrator_group_permissions(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    permission = apps.get_model('auth', 'Permission')

    if group.objects.filter(name='Administrators').exists():
        administrators = group.objects.get(name='Administrators')

        for perm in ['ingredient', 'recipe', 'recipeingredients']:
            for action in ['add', 'change', 'delete', 'view']:
                administrators.permissions.add(
                    permission.objects.get(codename=f'{action}_{perm}')
                )


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_create_recipes_permissions'),
    ]

    operations = [
        migrations.RunPython(administrator_group_permissions)
    ]

    if global_apps.is_installed('users'):
        dependencies.append(('users', '0003_administrator_group'))
