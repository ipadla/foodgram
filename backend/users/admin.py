from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'last_name', 'first_name', 'password')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('role',),
        }),
    )

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
    list_editable = (
        'last_name',
        'first_name',
        'role'
    )
    list_filter = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'last_name', 'first_name')

