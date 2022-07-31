from django.contrib.auth import get_user_model
from django.db import models

from tags.models import Tags

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    measurement_unit = models.CharField(max_length=16, null=False, blank=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "ingredients"

    def __str__(self):
        return self.name


def image_directory_path(instance, filename):
    return f'recipe_image/{filename}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=128, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    tags = models.ManyToManyField(Tags, blank=False)
    image = models.ImageField(upload_to=image_directory_path)
    cooking_time = models.PositiveSmallIntegerField(blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "recipes"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Recipe, self).delete(*args, **kwargs)
        storage.delete(path)


class RecipeFavorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        verbose_name_plural = 'recipe favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'recipe ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]
