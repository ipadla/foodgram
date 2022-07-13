from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('A', 'Admin'),
        ('U', 'User'),
    )

    first_name = models.CharField('first name', max_length=150, blank=False, null=False)
    last_name = models.CharField('last name', max_length=150, blank=False, null=False)
    email = models.EmailField('email address', max_length=254, blank=False, null=False)
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
