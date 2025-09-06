from django.core.exceptions import PermissionDenied

from .models import Profile, Venue, VenueStaffMember 

class VenueOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        user = Profile.objects.get(user = request.user)
        if not user.is_venue_owner:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

class AlreadyHasVenueMixin:
    def dispatch(self, request, *args, **kwargs):
        venue = Venue.objects.get(owner=request.user)
        if venue:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
    
class UserHasPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        user = Venue.objects.filter(owner=request.user).exists()
        staff = VenueStaffMember.objects.filter(user=request.user).exists()
        if not (user or staff):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)