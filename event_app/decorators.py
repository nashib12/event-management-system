from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Profile

def user_is_venue_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = Profile.objects.get(user = request.user)
        if user.is_venue_owner:
            return view_func
        else:
            messages.error(request, "Not a venue owner")
            return HttpResponseRedirect("/")
    return wrapper_func