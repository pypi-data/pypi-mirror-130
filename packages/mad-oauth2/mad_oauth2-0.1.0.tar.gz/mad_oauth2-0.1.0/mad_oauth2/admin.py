from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin

from mad_oauth2.models import Scope, Throttle

# Register your models here.

# @admin.register(Oauth2Application)
# class Oauth2ApplicationAdmin(ApplicationAdmin):
#     filter_horizontal = ('allowed_scopes',)
#     readonly_fields = ['id']
#     list_display = ['id', 'name', 'client_type', 'authorization_grant_type', 'created_at']



@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'key', 'throttling',]


@admin.register(Throttle)
class ThrottleAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'throttling', ]
