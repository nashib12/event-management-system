from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
# from formtools.wizard.views import SessionWizardView
# from django.utils.decorators import method_decorator

from .forms import *
from .models import *
# from .decorators import user_is_venue_owner
from .mixins import VenueOwnerMixin

class HomeView(TemplateView):
    template_name = "event_app/index.html"

#------------------- Authentication section -------------------------
class UserCreationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "authenticate/registration.html"
    success_url = reverse_lazy("create-profile")
    
    def form_valid(self, form):
        user = super().form_valid(form)
        
        login(self.request, self.object)
        
        return user
    
class ProfileCreationView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "authenticate/create_profile.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
# def show_venue_form(wizard):
#     cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
#     return cleaned_data.get('is_venue_owner')

# class ProfileCreationView(SessionWizardView):
#     form_list = [ProfileForm, VenueForm]
#     template_name = "authenticate/create_profile.html"
#     condition_dict = {"1" : show_venue_form}
#     success_url = reverse_lazy("home")
    
#     def done(self, form_list, **kwargs):
#         profile_form = form_list[0]
#         form = profile_form.save(commit=False)
#         form.user = self.request.user
#         form.save()
        
#         if profile_form.cleaned_data.get('is_venue_owner'):
#             venue_form = form_list[1]
#             venue = venue_form.save(commit=False)
#             venue.owner = self.request.user
#             venue.save()
        
#         return

class UserLoginView(LoginView):
    template_name = "authenticate/log_in.html"
    form_class = LoginForm
    redirect_authenticated_user = True

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = "authenticate/update_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("home")
    success_message = "Profile updated successfully!"

#------------------------------------ Venue Section ------------------------------------------    
class VenueCreationView(LoginRequiredMixin, VenueOwnerMixin, CreateView, SuccessMessageMixin):
    model = Venue
    form_class = VenueForm
    template_name = "venue/add_venue.html"
    success_url = reverse_lazy("home")
    success_message = "Venue Created Successfully"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class UpdateVenueView(LoginRequiredMixin, VenueOwnerMixin, UpdateView, SuccessMessageMixin):
    model = Venue
    form_class = VenueForm
    template_name = "venue/update_venue.html"
    success_url = reverse_lazy("view-venue")
    success_message = "Venue updated successfully"
    
class VenueView(ListView, LoginRequiredMixin):
    model = Venue
    template_name = "venue/venue.html"
    context_object_name = "venues"
    
    def get_queryset(self):
        return Venue.objects.filter(owner=self.request.user)
    
#--------------------------------------- Event Section ------------------------------------
class EventCreationView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_app/event_create.html"
    success_url = reverse_lazy("home")
    

    
        
