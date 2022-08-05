import json
import pytest

from recipes.models import Ingredient, Recipe, RecipeFavorites, ShoppingCart
from tags.models import Tags


class TestRecipesApi:
    @pytest.mark.django_db()
    def test_recipes(self, client, client_admin, client_user1, user1):
        response = client.get('/api/recipes/')
        assert response.status_code == 200
        assert len(response.json()['results']) == 0

        assert Recipe.objects.filter().count() == 0
        recipe = {
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            'name': 'mollit culpa eu',
            'text': 'sit Lorem in Ut',
            'cooking_time': 5818,
            'ingredients': [
                {'id': 1, 'amount': 12}
            ],
            'tags': [
                1
            ],
        }

        response = client_admin.post(
            '/api/recipes/',
            format='json',
            data=recipe
        )

        assert response.status_code == 201, f'{response.json()}'
        assert Recipe.objects.filter().count() == 1

        assert client_admin.get('/api/recipes/1/').status_code == 200
        assert client_user1.get('/api/recipes/1/').status_code == 200
        assert client.get('/api/recipes/1/').status_code == 200

        assert client_user1.delete('/api/recipes/1/').status_code == 403
        assert client.delete('/api/recipes/1/').status_code == 401

        assert RecipeFavorites.objects.filter(user=user1).exists() is False
        response = client_user1.post('/api/recipes/1/favorite/')
        assert response.status_code == 201
        assert response.json().get('id') == 1
        assert RecipeFavorites.objects.filter(user=user1).exists() is True

        assert client_admin.delete('/api/recipes/1/').status_code == 204
        assert Recipe.objects.filter().count() == 0
