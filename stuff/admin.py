from django.contrib import admin
from stuff.models import Role, PermissionModules, RolePermissions


admin.site.register(Role)
admin.site.register(PermissionModules)
admin.site.register(RolePermissions)
