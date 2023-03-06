from django.contrib import admin

from users.models import User, EmailVerification
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'email')
    fields = ('username', ('first_name', 'last_name', 'email'), 
              ('is_superuser', 'is_staff', 'is_active'), 'groups', 
              'user_permissions', ('last_login', 'date_joined'), 'image')
    search_fields = ('username', 'id', 'first_name', 'last_name', 'email')
    readonly_fields = ('username', 'first_name', 'last_name', 'email', 
                       'last_login', 'date_joined', 'image')
    inlines = (BasketAdmin, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('code', 'user', 'expiration', 'created')
