from django.contrib import admin

from djangoProject.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['title', 'username', 'email', 'name']
    list_display = ['id', 'username', 'name']
    search_fields = ['name', 'id']
