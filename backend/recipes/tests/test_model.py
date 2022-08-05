import pytest

from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)
from tags.models import Tags


class TestRecipesModel:
    @pytest.mark.django_db(transaction=True)
    def test_ingredient_creation(self):
        for i in range(5):
            Ingredient.objects.create(
                name=f'яйца иволги {i}',
                measurement_unit='шт'
            )

        assert Ingredient.objects.filter().count() == 10

    @pytest.mark.django_db(transaction=True)
    def test_recipe_creation(self, user1, tags):
        tag = Tags.objects.create(
            name=f'Tag',
            color=f'#EE00E2',
            slug=f'tag'
        )

        recipes_before = Recipe.objects.filter().count()
        for i in range(5):
            recipe = Recipe.objects.create(
                author=user1,
                name=f'Рецепт {i}',
                text='TRtrtrtrtr',
                cooking_time=i
            )

            recipe.tags.add(tag)

        assert Recipe.objects.filter().count() == recipes_before + 5

    @pytest.mark.django_db()
    def test_recipe_related_models(self, user1):
        assert Tags.objects.filter().count() == 5
        assert Ingredient.objects.filter().count() == 5

        recipe = Recipe.objects.create(
            author=user1,
            name=f'Рецепт 1',
            text='TRtrtrtrtr',
            cooking_time=16
        )

        recipe.tags.add(Tags.objects.get(id=1))
        recipe.tags.add(Tags.objects.get(id=2))

        assert RecipeIngredients.objects.filter(recipe=recipe).exists() is False
        RecipeIngredients.objects.create(
            ingredient=Ingredient.objects.get(id=1),
            recipe=recipe,
            amount=16
        )
        assert RecipeIngredients.objects.filter(recipe=recipe).exists() is True

        assert RecipeFavorites.objects.filter().count() == 0
        RecipeFavorites.objects.create(
            user=user1,
            recipe=recipe
        )
        assert RecipeFavorites.objects.filter().count() == 1

        assert ShoppingCart.objects.filter().count() == 0
        ShoppingCart.objects.create(
            user=user1,
            recipe=recipe
        )
        assert ShoppingCart.objects.filter().count() == 1

