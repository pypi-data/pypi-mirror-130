from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin

from mad_oauth2.models import Application, Scope, Throttle

# Register your models here.

@admin.register(Application)
class ApplicationAdminClass(ApplicationAdmin):
    filter_horizontal = ('scopes',)
    readonly_fields = ['id']
    list_display = ['id', 'name', 'client_type', 'authorization_grant_type', 'created_at']



@admin.register(Scope)
class ScopeAdminClass(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'key', 'throttling',]


@admin.register(Throttle)
class ThrottleAdminClass(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'throttling', ]
