from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'phone']
    fieldsets = (
        (None, {'fields': ['email', 'password', 'phone']}),
        (_('Personal Info'), {'fields': ('name','sacco','assigned_vehicle', 'role',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Sacco)
admin.site.register(models.Vehicle)
admin.site.register(models.Routes)
admin.site.register(models.VehicleType)
admin.site.register(models.VehicleTrip)
admin.site.register(models.PassengerTrip)
admin.site.register(models.PaymentMethod)
admin.site.register(models.Payment)
admin.site.register(models.Seats)
admin.site.register(models.Wallet)
