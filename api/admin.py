from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Video, Rating, Comment

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'followers_count', 'following_count', 'videos_count', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['created_at']

    # Custom fields for the user profile page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'website_url', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

# Registering CustomUser model with the custom UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Registering other models
admin.site.register(Video)
admin.site.register(Rating)
admin.site.register(Comment)
