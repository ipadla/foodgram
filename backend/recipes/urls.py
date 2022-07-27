from rest_framework import routers

from recipes.viewsets import (IngredientsViewSet, RecipesViewSet,
                              SubscriptionViewSet)

app_name = 'recipes'

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(
    r'users/subscription',
    SubscriptionViewSet,
    basename='subscription'
)

urlpatterns = router.urls
