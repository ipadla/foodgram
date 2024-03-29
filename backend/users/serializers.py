from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    ''' Сериализатор пользователя, только для чтения.
    Выдаёт основные поля.
    is_subscribed - метод сериализатора, возвращает существование записи в
    модели Subscription

    Не используем кортеж в Meta.fields - этот сериализатор наследуется с
    изменением полей использование кортежа - всё ломает.
    '''
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False

        user = request.user

        return Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()


class UserPasswordSerializer(serializers.Serializer):
    ''' Сериализатор смены пароля пользователя.
    Проверяет валидность пароля current_password
    Проверяет сложность пароля по Django'вски
    '''
    current_password = serializers.CharField(max_length=150, required=True)
    new_password = serializers.CharField(max_length=150, required=True)

    def validate_current_password(self, value):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            raise serializers.ValidationError('You are not authenticated')

        if not request.user.check_password(value):
            raise serializers.ValidationError('Wrong current_password')

        return value

    def validate_new_password(self, value):
        validate_password(value)

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            raise serializers.ValidationError('You are not authenticated')

        request.user.set_password(validated_data['new_password'])
        request.user.save()

        return request.user


class UserSignupSerializer(serializers.ModelSerializer):
    ''' Регистрация пользователя.
    Все поля обязательны.
    username <-> email должно быть уникальным
    username не может быть me
    Проверяется существование записей с таки email или username
    Проверяется сложность пароля
    '''

    email = serializers.EmailField(
        max_length=256,
        required=True
    )

    first_name = serializers.CharField(
        max_length=150,
        required=True
    )

    last_name = serializers.CharField(
        max_length=150,
        required=True
    )

    username = serializers.CharField(
        max_length=150,
        required=True
    )

    password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        read_only_fields = ('id',)

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(), fields=['email', 'username']
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'You cant use "me" as username'
            )

        return value

    def validate_password(self, value):
        validate_password(value)

        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            if (
                data['username']
                != User.objects.get(email=data['email']).username
            ):
                raise serializers.ValidationError(
                    'This email already used'
                )

        if User.objects.filter(username__iexact=data['username']).exists():
            if (
                data['email']
                != User.objects.get(username=data['username']).email
            ):
                raise serializers.ValidationError(
                    'This username already used'
                )

        return super().validate(data)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
