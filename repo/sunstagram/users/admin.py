from django.contrib import admin

# Register your models here.
from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email', 'username')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UsersAdmin)
