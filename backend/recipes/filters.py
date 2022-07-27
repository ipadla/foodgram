from django_filters import filterset

from recipes.models import Recipe


class RecipesFilter(filterset.FilterSet):
    is_favorited = filterset.BooleanFilter(
        label='is_favorited',
        method='recipe_favorited'
    )

    is_in_shopping_cart = filterset.BooleanFilter(
        label='is_in_shopping_cart',
        method='recipe_in_shopping_cart'
    )

    tags = filterset.CharFilter(
        method='recipe_tags'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def recipe_favorited(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset.filter()
        if value is True:
            user_favorites = self.request.user.favorite.all()
            return queryset.filter(
                id__in=user_favorites.values_list(
                    'recipe__id',
                    flat=True
                )
            )

        return queryset.filter()

    def recipe_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset.filter()
        if value is True:
            user_shopping_cart = self.request.user.shopping_cart.all()
            return queryset.filter(
                id__in=user_shopping_cart.all().values_list(
                    'recipe__id',
                    flat=True
                )
            )

        return queryset.filter()

    def recipe_tags(self, queryset, name, value):
        return queryset.filter(
            tags__slug__in=self.request.query_params.getlist(name)
        )
