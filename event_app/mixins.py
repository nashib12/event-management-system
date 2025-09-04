from django.core.exceptions import PermissionDenied

from .models import Profile

class VenueOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        user = Profile.objects.get(user = request.user)
        if not user.is_venue_owner:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)