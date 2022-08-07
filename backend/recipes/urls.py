from rest_framework import routers

from .viewsets import IngredientsViewSet, RecipesViewSet, SubscriptionViewSet

app_name = 'recipes'

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register(
    'users/subscriptions',
    SubscriptionViewSet,
    basename='subscription'
)

urlpatterns = router.urls
