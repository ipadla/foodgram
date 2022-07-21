import pytest

from users.models import Subscription


@pytest.mark.django_db(transaction=True)
class TestUsersSubscriptionModel:
    def test_users_follow_model_fields(self):
        expected_fields = ['author', 'user']

        for field in expected_fields:
            assert field == Subscription._meta.get_field(field).name


@pytest.mark.django_db(transaction=True)
class TestUsersSubscription:
    def test_unauthorized_subscription(self, client, user1):
        url = f'/api/users/{user1.id}/subscribe/'

        assert client.get(url).status_code == 401
        assert client.post(url).status_code == 401
        assert client.delete(url).status_code == 401

    def test_authorized_subscription(
        self, client_user1, client_user2, user1, user2
    ):
        url = f'/api/users/{user1.id}/subscribe/'

        response = client_user1.post(url)
        assert response.status_code == 400, f'{response.json()}'

        assert Subscription.objects.filter(
            user=user2,
            author=user1
        ).exists() is False

        assert client_user2.post(url).status_code == 201
        assert Subscription.objects.filter(
            user=user2,
            author=user1
        ).exists() is True
        assert user2.subscriber.all().count() == 1
        assert user1.subscribed.all().count() == 1

        response = client_user2.get(f'/api/users/{user1.id}/')
        assert response.status_code == 200
        assert 'is_subscribed' in response.json()
        assert response.json()['is_subscribed'] is True

        response = client_user2.post(url)
        assert response.status_code == 400, f'{response.json()}'

        assert client_user2.delete(url).status_code == 204
        assert Subscription.objects.filter(
            user=user2,
            author=user1
        ).exists() is False
        assert user2.subscriber.all().count() == 0
        assert user1.subscribed.all().count() == 0

        response = client_user2.get(f'/api/users/{user1.id}/')
        assert response.status_code == 200
        assert 'is_subscribed' in response.json()
        assert response.json()['is_subscribed'] is False

        response = client_user2.delete(url)
        assert response.status_code == 404, f'{response.json()}'
