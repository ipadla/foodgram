from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context['request'].user,
            author=obj
        ).exists()


class UserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=150, required=True)
    new_password = serializers.CharField(max_length=150, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('Wrong current_password')

        return value

    def validate_new_password(self, value):
        validate_password(value)

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()

        return user


class UserSignupSerializer(serializers.ModelSerializer):

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
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
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
