from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin
from mad_oauth2.models import Application, Scope, Throttle

import logging
logger = logging.getLogger(__name__)

# Register your models here.

try:
    admin.site.unregister(Application)
except Exception as e:
    logger.error(str(e))
    pass

try:
    @admin.register(Application)
    class ApplicationAdminClass(ApplicationAdmin):
        filter_horizontal = ('scopes',)
        readonly_fields = ['id']
        list_display = ['id', 'name', 'client_type', 'authorization_grant_type', 'created_at']
except Exception as e:
    logger.error(str(e))
    pass


@admin.register(Scope)
class ScopeAdminClass(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'key', 'throttling',]


@admin.register(Throttle)
class ThrottleAdminClass(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'name', 'throttling', ]
