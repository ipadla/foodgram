from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import (UserPasswordSerializer, UserSerializer,
                               UserSignupSerializer)

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        uid = self.kwargs.get('id', None)

        if uid == 'me':
            uid = self.request.user.id

        return get_object_or_404(User, id=uid)

    def get_permissions(self):
        permissions = self.permission_classes

        if self.action in ['create', 'list']:
            permissions = [AllowAny]
            return [permission() for permission in permissions]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignupSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = UserPasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
