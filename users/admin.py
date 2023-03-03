from django.contrib import admin

from users.models import User
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
