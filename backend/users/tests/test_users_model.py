from django.contrib.auth import get_user_model
from django.db.models import fields

User = get_user_model()


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


class TestUsersModel:
    def test_users_model_fields(self):
        expected_fields = {
            'role': fields.CharField,
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
