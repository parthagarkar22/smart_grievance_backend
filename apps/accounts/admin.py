
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'mobile',
        'role',
        'department',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'department',
        'is_active',
    )

    search_fields = (
        'username',
        'mobile',
    )

    fieldsets = (
        ('Basic Info', {
            'fields': ('username', 'password', 'mobile')
        }),
        ('Role & Department', {
            'fields': ('role', 'department')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    readonly_fields = ('last_login', 'date_joined')
