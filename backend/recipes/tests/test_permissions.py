import pytest
from django.contrib.auth.models import Group, Permission


class TestRecipesPermissions:
    @pytest.mark.django_db(transaction=True)
    def test_administrators_group_permissions(self, admin):
        group = Group.objects.get(name='Administrators')
        assert group is not None
        assert group in admin.groups.all()

        for perm in [
            'ingredient', 'recipe', 'recipeingredients'
        ]:
            for action in ['add', 'change', 'delete', 'view']:
                permission = Permission.objects.get(codename=f'{action}_{perm}')
                assert admin.has_perm(
                    f'recipes.{permission.codename}'
                ) is True, f'Administrator lack {permission.codename}'
