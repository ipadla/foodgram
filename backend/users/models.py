from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('A', 'Admin'),
        ('U', 'User'),
    )

    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=False,
        null=False
    )

    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=False,
        null=False
    )

    email = models.EmailField(
        'email address',
        max_length=254,
        blank=False,
        null=False,
        unique=True
    )

    role = models.CharField(
        max_length=1,
        choices=USER_ROLES,
        default='U'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_username'
            )
        ]
        ordering = ('-date_joined',)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Последователь',
        help_text='Пользователь который подписывается'
    )

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Автор',
        help_text='Пользователь на которого подписываются'
    )
