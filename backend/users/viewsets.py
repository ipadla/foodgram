from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .permissions import IsNotAuthenticated
from .serializers import (UserPasswordSerializer, UserSerializer,
                          UserSignupSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permissions = self.permission_classes

        if self.action == 'create':
            permissions = [IsNotAuthenticated]
            return [permission() for permission in permissions]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignupSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = UserPasswordSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete', 'post'])
    def subscribe(self, request, id=None):
        """ Управление подписками пользователя.
        Если пользователь пытается подписаться на себя - отругать.
        DELETE: Если подписка существует - удалить
        POST: Если подписка не существует - создаем, иначе - ругаемся.
        """
        author = self.get_object()
        if request.user == author:
            return Response(
                data={'errors': 'Нельзя это делать с самим собой.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = Subscription.objects.filter(
            author=author,
            user=request.user
        )

        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                data={'detail': 'Подписка не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    data={'errors': 'Подписка уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.create(author=author, user=request.user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
