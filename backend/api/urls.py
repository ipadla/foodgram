from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('recipes.urls', namespace='recipes')),
    path('', include('tags.urls', namespace='tags')),
    path('', include('users.urls', namespace='users')),
    path('auth/', include('djoser.urls.authtoken'))
]
