from django.db.models import Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.filters import RecipesFilter
from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)
from recipes.serializers import (IngredientSerializer,
                                 RecipeFavoriteShoppingSerializer,
                                 RecipeSerializer,
                                 RecipeSubscriptionSerializer)
from users.models import User

class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    # TODO: Filters, Search, Pagination limit
    # TODO: actions decorator
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RecipesFilter
    lookup_field = 'id'
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        # TODO: download shopping_cart
        # TODO: prettify shopping_cart
        shopping_cart = request.user.shopping_cart.all()
        print(
            RecipeIngredients.objects.filter(
                recipe__id__in=shopping_cart.values_list('recipe__id', flat=True)
            ).values('ingredient__name', 'ingredient__measurement_unit').annotate(Sum('amount'))
        )
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['delete', 'post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id=None):
        recipe = self.get_object()

        favorited = RecipeFavorites.objects.filter(
            recipe=recipe,
            user=request.user
        )

        if request.method == 'DELETE':
            if favorited.exists():
                favorited.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                data={'detail': 'Избранное не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'POST':
            if favorited.exists():
                return Response(
                    data={'errors': 'Избранное уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            RecipeFavorites.objects.create(recipe=recipe, user=request.user)
            return Response(
                data=RecipeFavoriteShoppingSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete', 'post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id=None):
        recipe = self.get_object()

        shop_carted = ShoppingCart.objects.filter(
            recipe=recipe,
            user=request.user
        )

        if request.method == 'DELETE':
            if shop_carted.exists():
                shop_carted.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                data={'detail': 'Рецепт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'POST':
            if shop_carted.exists():
                return Response(
                    data={'errors': 'Рецепт уже в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(recipe=recipe, user=request.user)
            return Response(
                data=RecipeFavoriteShoppingSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: ListOnly
    serializer_class = RecipeSubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            id__in=self.request.user.subscriber.all().values_list(
                'author__id',
                flat=True
            )
        )
