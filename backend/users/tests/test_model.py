import pytest
from django.contrib.auth.models import Group
from django.db.models import fields

from tests.common import User


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


@pytest.mark.django_db(transaction=True)
class TestUsersModel:
    def test_users_model_fields(self):
        expected_fields = {
            'role': fields.PositiveSmallIntegerField,
            'email': fields.EmailField,
            'username': fields.CharField,
            'first_name': fields.CharField,
            'last_name': fields.CharField
        }

        model_fields = User._meta.fields

        for key, value in expected_fields.items():
            field = search_field(model_fields, key)
            assert field is not None, f'No field "{key}" in User model'
            assert type(field) == value, (
                f'Field {key} should be {value} type.'
            )

    def test_users_model_create(self, password_1):
        user, _ = User.objects.get_or_create(
            username='userTest1',
            email='testuser1@mail.fake',
            password=password_1,
            first_name='Common',
            last_name='User'
        )
        group = Group.objects.get(name='Administrators')

        assert user is not None
        assert group not in user.groups.all()
        assert user.is_staff is False

        user.role = User.ADMIN
        user.save()

        assert group in user.groups.all()
        assert user.is_staff is True

        user.role = User.USER
        user.save()

        assert group not in user.groups.all()
        assert user.is_staff is False
