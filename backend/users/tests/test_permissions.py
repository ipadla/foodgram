from django.contrib.auth.models import Group
import pytest


class TestUsersPermissions:
    @pytest.mark.django_db
    def test_administrators_group(self, admin, user1):
        assert Group.objects.filter(name='Administrators').exists() is True

    @pytest.mark.django_db
    def test_administrators_group_permissions(self, admin, user1):
        group = Group.objects.get(name='Administrators')
        assert group is not None
        assert group in admin.groups.all()
        assert group not in user1.groups.all()

        assert admin.has_perm('users.add_user') is True
        assert admin.has_perm('users.change_user') is True
        assert admin.has_perm('users.delete_user') is True
        assert admin.has_perm('users.view_user') is True

    @pytest.mark.django_db
    def test_administrators_permissions(self, admin):
        assert admin.is_staff is True
