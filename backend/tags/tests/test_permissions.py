import pytest
from django.contrib.auth.models import Group


class TestTagsPermissions:
    @pytest.mark.django_db(transaction=True)
    def test_administrators_group_permissions(self, admin):
        group = Group.objects.get(name='Administrators')
        assert group is not None
        assert group in admin.groups.all()

        assert admin.has_perm('tags.add_tags') is True
        assert admin.has_perm('tags.change_tags') is True
        assert admin.has_perm('tags.delete_tags') is True
        assert admin.has_perm('tags.view_tags') is True
