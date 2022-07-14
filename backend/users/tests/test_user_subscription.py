import pytest

from users.models import Follow

class TestUsersSubscription:
    @pytest.mark.django_db(transaction=True)
    def test_user_subscription(self, client, client_user, client_user2, user, user2):
        url = f'/api/users/{user.id}/subscribe/'

        assert client.get(url).status_code == 401, (
            'Unauthorized users can\'t use subscriptions'
        )

        response = client_user.post(url)
        assert response.status_code == 400, (
            f'{response.json()["errors"]}'
        )

        follow_objects = Follow.objects.all().count()
        assert client_user2.post(url).status_code == 201
        assert Follow.objects.all().count() == follow_objects + 1
        assert client_user2.delete(url).status_code == 204
        assert Follow.objects.all().count() == follow_objects
