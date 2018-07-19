from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from django.db.models.expressions import F
from .models import Profile
from django.utils.deprecation import MiddlewareMixin

class LastActivityMiddleware(MiddlewareMixin):
    KEY = "last-activity"

    def process_request(self, request):
        if not hasattr(request, 'user'):
            return response
        if request.user.is_authenticated:
                Profile.objects.filter(user_id=request.user.id).update(last_activity=timezone.now())
        return None

        #  def process_view(self, request, view_func, view_args, view_kwargs):
        # assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        # if request.user.is_authenticated():
        #     Profile.objects.filter(user__id=request.user.id) \
        #                    .update(last_activity=timezone.now())
