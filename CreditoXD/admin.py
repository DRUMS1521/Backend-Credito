from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from empleados.models import Empleados


class EmpleadoAdmin(UserAdmin):
    list_display = ('cedula', 'is_active')
    search_fields = ('cedula',)
    fieldsets = (
        (None, {'fields': ('cedula', 'contraseña')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula', 'contraseña', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(Empleado, EmpleadoAdmin)
