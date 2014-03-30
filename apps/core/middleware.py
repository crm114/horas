import pytz

from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')

        if tzname:
            timezone.activate(pytz.timezone(tzname))

        elif request.user.is_authenticated():
            try:
                tzname = request.user.timezone
                timezone.activate(pytz.timezone(tzname))
            except Exception as e:
                print('Failed to set timezone', e)
        else:
            timezone.deactivate()


class EnsureCompleteProfileMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            update_url = str(reverse_lazy('profile_update', args=[request.user.username]))

            if not request.user.has_complete_profile() and request.path != update_url:
                messages.info(request, _('Debes completar tu perfil para continuar'))
                return HttpResponseRedirect(update_url)


