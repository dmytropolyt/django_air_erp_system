from django.contrib import admin
from django.contrib.auth.models import User
from .models import Flight, Ticket, Option, Seat, GateRegistration, CheckIn


class StaffAdminArea(admin.AdminSite):
    site_header = 'DjangoAir Staff'


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'first_name', 'last_name')
        }),
        ('Staff Groups', {
            'fields': ('is_staff', 'groups')
        })
    )
    # fields = ('is_staff', 'groups')
    readonly_fields = ('username', 'first_name', 'last_name')
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_editable = ('is_staff',)


staff_site = StaffAdminArea(name='StaffAdmin')
staff_site.register(User, UserAdmin)
staff_site.register(Flight)
staff_site.register(Ticket)
staff_site.register(Option)
staff_site.register(GateRegistration)
staff_site.register(CheckIn)

admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Option)
admin.site.register(Seat)
