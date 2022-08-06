from django.contrib import admin
from .models import UserAccount,Address, FAQ, Reports
# Register your models here.

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',  'phone', 'is_active', 'is_staff',)
    search_fields=('first_name', 'last_name', 'email',  'phone',)

@admin.register(Address)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','address_line1','address_line2','city','state','pin_code')


@admin.register(FAQ)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','question','answer')

@admin.register(Reports)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','complaint')
