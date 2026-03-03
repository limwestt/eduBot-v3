from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "xp", "streak_days")
    search_fields = ("user__username", "user__email")
