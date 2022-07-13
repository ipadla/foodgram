from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
    list_display_links = ['pk', 'username', 'email']
    list_filter = ['username', 'email', 'is_active', 'is_staff']
