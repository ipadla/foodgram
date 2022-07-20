import pytest

from users.models import Follow


class TestUsersSubscriptionModel:
    @pytest.mark.django_db
    def test_users_follow_model_fields(self):
        expected_fields = ['author', 'user']

        for field in expected_fields:
            assert field == Follow._meta.get_field(field).name


class TestUsersSubscription:
    @pytest.mark.django_db()
    def test_unauthorized_subscription(self, client, user1):
        url = f'/api/users/{user1.id}/subscribe/'

        assert client.get(url).status_code == 401
        assert client.post(url).status_code == 401
        assert client.delete(url).status_code == 401

    @pytest.mark.django_db(transaction=True)
    def test_authorized_subscription(self, client_user1, client_user2, user1):
        url = f'/api/users/{user1.id}/subscribe/'

        response = client_user1.post(url)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        follow_objects = Follow.objects.all().count()
        assert client_user2.post(url).status_code == 201
        assert Follow.objects.all().count() == follow_objects + 1

        response = client_user2.post(url)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        assert client_user2.delete(url).status_code == 204
        assert Follow.objects.all().count() == follow_objects

        response = client_user2.delete(url)
        assert response.status_code == 404, (
            f'{response.json()}'
        )
