from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import *


class HomeView(TemplateView):
    template_name = "event_app/index.html"
    
class UserCreationView(FormView):
    template_name = "event_app/registration.html"
    form_class = CustomUserCreationForm
    success_url = "/home/"
    
class ProfileCreationView(FormView):
    template_name = "event_app/profile_create.html"
    form_class = ProfileForm
    success_url = "/home/"
    
class VenueCreationView(FormView):
    template_name = "event_app/venue_create.html"
    form_class = VenueForm
    success_url = "/home/"
    
class EventCreationView(FormView):
    template_name = "event_app/event_create.html"
    form_class = EventForm
    success_url = "/home/"
    
        
