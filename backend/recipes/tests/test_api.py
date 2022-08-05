import json
import pytest

from recipes.models import Ingredient, Recipe, RecipeFavorites, ShoppingCart
from tags.models import Tags


class TestRecipesApi:
    @pytest.mark.django_db()
    def test_recipes(self, client, client_admin, client_user1, user1):
        response = client.get('/api/recipes/')
        assert response.status_code == 200

        recipes_before = Recipe.objects.filter().count()
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

        recipe_id = response.json().get('id')

        assert response.status_code == 201, f'{response.json()}'
        assert Recipe.objects.filter().count() == recipes_before + 1

        assert client_admin.get('/api/recipes/1/').status_code == 200
        assert client_user1.get('/api/recipes/1/').status_code == 200
        assert client.get('/api/recipes/1/').status_code == 200

        assert client_user1.delete(f'/api/recipes/{recipe_id}/').status_code == 403
        assert client.delete('/api/recipes/1/').status_code == 401

        assert client_admin.delete(f'/api/recipes/{recipe_id}/').status_code == 204
        assert Recipe.objects.filter().count() == recipes_before

    @pytest.mark.django_db()
    def test_recipes_favorite(self, client, client_admin, client_user1, user1):
        url = '/api/recipes/1/favorite/'

        assert client.delete(url).status_code == 401
        assert client.post(url).status_code == 401

        assert RecipeFavorites.objects.filter(user=user1).exists() is False

        response = client_user1.post(url)
        assert response.status_code == 201
        assert response.json().get('id') == 1
        assert RecipeFavorites.objects.filter(user=user1).exists() is True

        response = client_user1.delete(url)
        assert response.status_code == 204
        assert RecipeFavorites.objects.filter(user=user1).exists() is False

    @pytest.mark.django_db()
    def test_recipes_shopping_cart(self, client, client_admin, client_user1, user1):
        url = '/api/recipes/1/shopping_cart/'

        assert client.delete(url).status_code == 401
        assert client.post(url).status_code == 401

        assert ShoppingCart.objects.filter(user=user1).exists() is False

        response = client_user1.post(url)
        assert response.status_code == 201
        assert response.json().get('id') == 1

        assert ShoppingCart.objects.filter(user=user1).exists() is True

        download_url='/api/recipes/download_shopping_cart/'
        response = client_user1.get(
            download_url,
            headers={
                'Accept': 'application/pdf'
            }
        )
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'

        response = client_user1.delete(url)
        assert response.status_code == 204
        assert ShoppingCart.objects.filter(user=user1).exists() is False

        response = client_user1.get(
            download_url,
            headers={
                'Accept': 'application/txt'
            }
        )
        assert response.status_code == 404

        response = client.get(
            download_url,
            headers={
                'Accept': 'application/txt'
            }
        )

        assert response.status_code == 401
