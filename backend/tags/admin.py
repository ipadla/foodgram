from django.contrib import admin

from .models import Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_display_links = ('id', 'name', 'color', 'slug')
