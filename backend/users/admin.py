from django.contrib import admin, auth

from .models import Subscription, User


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    ''' Административный интерфейс пользователей.

    В зависимости от роли пользователя на редактирование выдаёт только
    определенные поля.

    Редактирование суперпользователя возможно только суперпользователем.
    '''
    empty_value_display = '-empty-'

    list_display = (
        'pk',
        'username',
        'email',
        'last_name',
        'first_name',
        'role',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    list_display_links = ('pk', 'username', 'email')

    list_filter = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    search_fields = ('username', 'email', 'last_name', 'first_name')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2'
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser and obj is not None:
            return UserAdmin.fieldsets + (
                ('Advanced options', {'fields': ('role', )}),
            )

        if request.user.is_staff and request.user.role == User.ADMIN:
            return (
                (None, {
                    'fields': (
                        'password',
                        'is_active'
                    )
                }),
            )

        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id',)
    list_filter = ('user', 'author')
