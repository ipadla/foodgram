from tests.common import BASE_DIR
import pytest

from recipes.models import Ingredient, Recipe, RecipeIngredients
from tags.models import Tags


@pytest.fixture(autouse=True)
def recipes(django_db_blocker, tags, ingredients, user1):
    with django_db_blocker.unblock():
        for i in range(5):
            Recipe.objects.create(
                author=user1,
                name=f'Recipe {i}',
                text=f'Recipe {i} text',
                cooking_time=64 + i,
                image=f'{BASE_DIR}/media/tmp/tt.jpg'
            )
