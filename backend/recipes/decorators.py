from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from recipes.serializers import RecipeFavoriteShoppingSerializer


def favorite_and_cart(model=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, id=None):
            if model is None:
                return func(self, request, id=None)

            recipe = self.get_object()

            obj = model.objects.filter(
                recipe=recipe,
                user=request.user
            )

            if request.method == 'DELETE':
                if obj.exists():
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

                return Response(
                    data={'detail': 'Избранное не найдено.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if request.method == 'POST':
                if obj.exists():
                    return Response(
                        data={'errors': 'Избранное уже существует.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                model.objects.create(recipe=recipe, user=request.user)
                return Response(
                    data=RecipeFavoriteShoppingSerializer(recipe).data,
                    status=status.HTTP_201_CREATED
                )

            return func(self, request, id=None)
        return wrapper
    return decorator
