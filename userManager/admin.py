from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class AccountAdmin(UserAdmin):
    def get_friends(self, obj):
        return ", ".join([str(p) for p in obj.friends.all()])

    list_display = ('email', 'first_name', 'last_name', 'alias', 'dateOfBirth', 'get_friends')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    search_fields = ('email', 'first_name', 'last_name', 'alias', 'dateOfBirth', 'friends')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'alias', 'password1', 'password2', 'dateOfBirth', 'friends'),
        }),
    )


admin.site.register(User, AccountAdmin)
