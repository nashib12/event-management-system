from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import *
from .models import *

class HomeView(TemplateView):
    template_name = "event_app/index.html"

#------------------- Authentication section -------------------------
class UserCreationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "authenticate/registration.html"
    success_url = reverse_lazy("home")
    
class ProfileCreationView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "event_app/profile_create.html"
    success_url = reverse_lazy("home")

#------------------------------------ Venue Section ------------------------------------------    
class VenueCreationView(CreateView):
    model = Venue
    form_class = VenueForm
    template_name = "event_app/venue_create.html"
    success_url = reverse_lazy("home")
    
#--------------------------------------- Event Section ------------------------------------
class EventCreationView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_app/event_create.html"
    success_url = reverse_lazy("home")
    

    
        
