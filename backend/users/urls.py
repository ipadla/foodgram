from rest_framework import routers

from .viewsets import UsersViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = router.urls
