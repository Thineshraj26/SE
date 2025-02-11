from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import Item, Account

admin.site.register(Item)

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    ordering = ("username",)