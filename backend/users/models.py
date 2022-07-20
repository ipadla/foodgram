from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):

    ADMIN = 1
    USER = 2

    USER_ROLES = (
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    )

    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=False,
        null=False,
        help_text=('Required. 150 characters or fewer. Letters only.'),
    )

    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=False,
        null=False,
        help_text=('Required. 150 characters or fewer. Letters only.'),
    )

    email = models.EmailField(
        'email address',
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        help_text=(
            'Required. Max 254 characters. Letters, digits and @/./+/-/_ only.'
        ),
    )

    role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=USER)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'], name='unique_email_username'
            )
        ]
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if self.role == User.ADMIN:
            self.is_staff = True
        elif self.is_superuser is False and self.role != User.ADMIN:
            self.is_staff = False

        super().save(*args, **kwargs)


@receiver(models.signals.post_save, sender=User)
def check_user_in_administrators_group(sender, instance, using, **kwargs):
    if Group.objects.filter(name='Administrators').exists() is True:
        group = Group.objects.get(name='Administrators')

        if instance.role == User.ADMIN and group not in instance.groups.all():
            group.user_set.add(instance)

        if instance.role != User.ADMIN and group in instance.groups.all():
            group.user_set.remove(instance)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Последователь',
        help_text='Пользователь который подписывается',
    )

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Автор',
        help_text='Пользователь на которого подписываются',
    )
