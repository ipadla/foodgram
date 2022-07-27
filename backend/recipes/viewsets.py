from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.decorators import favorite_and_cart
from recipes.filters import RecipesFilter
from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)
from recipes.serializers import (IngredientSerializer,
                                 RecipeSerializer,
                                 RecipeSubscriptionSerializer)
from users.models import User


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    # TODO: Pagination limit
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
    @favorite_and_cart(model=RecipeFavorites)
    def favorite(self, request, id=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete', 'post'],
        permission_classes=[IsAuthenticated]
    )
    @favorite_and_cart(model=ShoppingCart)
    def shopping_cart(self, request, id=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = RecipeSubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            id__in=self.request.user.subscriber.all().values_list(
                'author__id',
                flat=True
            )
        )
