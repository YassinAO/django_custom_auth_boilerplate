from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdminConfig(UserAdmin):
    # model = Account

    search_fields = ('email', 'username')
    list_filter = ('is_admin', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('-username',)
    list_display = ('email', 'username', 'is_admin',
                    'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        ('Personal', {'fields': ('email', 'username',)}),
        ('Permissions', {'fields': ('is_admin',
                                    'is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(Account, UserAdminConfig)
