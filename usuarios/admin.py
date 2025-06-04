from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_verified', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'username')
    fieldsets = UserAdmin.fieldsets + (
        ('Verificación', {'fields': ('is_verified', 'verification_code')}),
    )
