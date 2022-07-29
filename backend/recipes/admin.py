from django.contrib import admin

from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorited')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'tags')
    search_fields = ('name', 'text')

    def favorited(self, obj):
        return RecipeFavorites.objects.filter(recipe=obj).count()


@admin.register(RecipeFavorites)
class RecipesFavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id',)
    list_filter = ('user', 'recipe')
    search_fields = ('recipe__name',)


@admin.register(RecipeIngredients)
class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_display_links = ('id',)
    list_filter = ('recipe',)
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(ShoppingCart)
class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id',)
    list_filter = ('user', 'recipe')
    search_fields = ('recipe__name',)
