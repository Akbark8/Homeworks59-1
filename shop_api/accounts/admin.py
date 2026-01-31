from django.contrib import admin
from .models import CustomUser, ConfirmationCode


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'birthdate', 'is_active')
    search_fields = ('email',)


@admin.register(ConfirmationCode)
class ConfirmationCode(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')