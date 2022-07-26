from django.contrib import admin, auth

from users.models import User, Subscription


class UserAdmin(auth.admin.UserAdmin):
    empty_value_display = '-empty-'

    list_display = (
        'pk',
        'username',
        'email',
        'last_name',
        'first_name',
        'role',
        'is_active',
        'is_staff'
    )

    list_display_links = ('pk', 'username', 'email')

    # list_editable = (
    #     'last_name',
    #     'first_name',
    #     'role'
    # )

    list_filter = ('username', 'email', 'is_active', 'is_staff')

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


admin.site.register(User, UserAdmin)

@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id',)

