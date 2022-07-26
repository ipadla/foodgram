from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)
from tags.serializers import TagsSerializer
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'amount']
        read_only_fields = ('id', 'recipe',)

    def to_internal_value(self, data):
        ingredient_id = data.get('id')
        internal_data = super().to_internal_value(data)

        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError()

        internal_data['ingredient'] = ingredient

        return internal_data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        ingredient_rep = rep.pop('ingredient')
        for key in ingredient_rep:
            rep[key] = ingredient_rep[key]
        return rep


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False
        else:
            user = request.user

        return RecipeFavorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False
        else:
            user = request.user

        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )

        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe, **ingredient
            )

        recipe.tags.set(tags)

        return recipe


class RecipeFavoriteShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ('__all__',)


class RecipeSubscriptionSerializer(UserSerializer):
    recipes = RecipeFavoriteShoppingSerializer(many=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'recipes'
        ]
        read_only_fields = ('__all__',)
