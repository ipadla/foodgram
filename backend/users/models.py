from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('A', 'Admin'),
        ('U', 'User'),
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
