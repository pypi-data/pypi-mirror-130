from mad_oauth2.models import Throttle
from mad_oauth2.settings import oauth2_settings
from rest_framework.throttling import ScopedRateThrottle
from mad_webhooks.application import getApplicationDataFromRequest

class ThrottleClass():
    def __init__(self):
        return dict(Throttle.objects.values_list('scope', 'rate'))


def getThrottling():
    throttling = oauth2_settings.THROTTLE_CLASS()
    return throttling


class BaseScopedRateThrottle(ScopedRateThrottle):
    THROTTLE_RATES = getThrottling()

    def __init__(self):
        super(BaseScopedRateThrottle, self).__init__()

    def get_cache_key(self, request, view):
        if request.user is not None and request.user.is_authenticated:
            ident = request.user.pk
        else:
            app_data = getApplicationDataFromRequest(self.request)
            ident = app_data['application'].id

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }