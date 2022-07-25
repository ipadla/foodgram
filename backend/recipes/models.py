from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    measurement_unit = models.CharField(max_length=16, null=False, blank=False)

    class Meta:
        verbose_name_plural = "ingredients"


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=False, blank=False)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "recipes"


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField()
