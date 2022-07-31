from django.conf import settings
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.utils import model_meta

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
    ingredients = RecipeIngredientsSerializer(many=True, required=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=True)
    tags = TagsSerializer(many=True, required=True, allow_null=False)
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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url
        return rep

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

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        ingredients = validated_data.pop('ingredients')

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        original_ingredients = list(
            instance.ingredients.all().values_list(
                'ingredient__id',
                flat=True
            )
        )

        for ingredient in ingredients:

            amount = ingredient.get('amount')
            ingredient_obj = ingredient.get('ingredient')

            if ingredient_obj.id not in original_ingredients:
                RecipeIngredients.objects.create(
                    ingredient=ingredient_obj,
                    recipe=instance,
                    amount=amount
                )
            else:
                RecipeIngredients.objects.filter(
                    recipe=instance,
                    ingredient=ingredient_obj
                ).update(amount=amount)

            try:
                original_ingredients.remove(
                    ingredient_obj.id
                )
            except ValueError:
                pass

        RecipeIngredients.objects.filter(
            recipe=instance,
            ingredient__id__in=original_ingredients
        ).delete()

        return instance

    def validate(self, data):
        tags = data.get('tags', None)
        if tags is None or not tags:
            raise serializers.ValidationError(
                'Tags cant be empty.'
            )

        ingredients = data.get('ingredients', None)
        if ingredients is None or not ingredients:
            raise serializers.ValidationError(
                'Ingredients cant be empty.'
            )

        return data


class RecipeFavoriteShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ('__all__',)


class RecipeSubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'recipes'
        ]
        read_only_fields = ('__all__',)

    def get_recipes(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return {}

        recipes_limit = request.query_params.get(
            'recipes_limit',
            settings.RECIPES_LIMIT
        )

        recipes_list = obj.recipes.all()[:int(recipes_limit)]
        serializer = RecipeFavoriteShoppingSerializer(recipes_list, many=True)

        return serializer.data
