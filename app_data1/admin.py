from django.contrib import admin

# Register your models here.
from .models import ActiveUser,ActivationKeys


@admin.register(ActiveUser)
class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(ActivationKeys)
class ActivationKeysAdmin(admin.ModelAdmin):
    list_display = ('activation_key','allocated_to','is_active')