from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
# from formtools.wizard.views import SessionWizardView
# from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .forms import *
from .models import *
# from .decorators import user_is_venue_owner
from .mixins import *

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

class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "authenticate/password_change.html"
    success_url = reverse_lazy("log-in")
    success_message = "Password changed successfully"

#------------------------------------ Venue Section ------------------------------------------    
class VenueCreationView(LoginRequiredMixin, VenueOwnerMixin, AlreadyHasVenueMixin, SuccessMessageMixin, CreateView):
    model = Venue
    form_class = VenueForm
    template_name = "venue/add_venue.html"
    success_url = reverse_lazy("view-venue")
    success_message = "Venue Created Successfully"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class UpdateVenueView(LoginRequiredMixin, VenueOwnerMixin, SuccessMessageMixin, UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = "venue/update_venue.html"
    success_url = reverse_lazy("view-venue")
    success_message = "Venue updated successfully"
    
class VenueView(LoginRequiredMixin, ListView):
    model = Venue
    template_name = "venue/venue.html"
    context_object_name = "venues"
    
    def get_queryset(self):
        return Venue.objects.filter(owner=self.request.user)
    
class VenueDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Venue
    success_url = reverse_lazy("view-venue")
    success_message = "Venue Deleted Successfully"
    template_name = "venue/venue_confirm_delete.html"

class VenueStaffCreateView(LoginRequiredMixin, SuccessMessageMixin, VenueOwnerMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    success_message = "Staff account successfully created"
    template_name = "venue/add_venue_staff.html"
    
    def form_valid(self, form):
        user = form.save()
        venue = Venue.objects.get(owner = self.request.user)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        VenueStaffMember.objects.create(user=user, venue=venue, first_name=first_name, last_name=last_name, email=email)
        return super().form_valid(form)
    
#--------------------------------------- Event Section ------------------------------------
class EventCreationView(LoginRequiredMixin, UserHasPermissionMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/add_event.html"
    success_url = reverse_lazy("events")
    success_message = "Event Successfully added"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            venue = Venue.objects.get(owner=self.request.user)
            instance.venue = venue
            instance.save()
        except Venue.DoesNotExist:
            staff = VenueStaffMember.objects.get(user=self.request.user)
            instance.venue = staff.venue
            instance.save()
        return super().form_valid(form)
    
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"
    template_name = "event/list_event.html"
    
    def get_queryset(self):
        try:
            venue = Venue.objects.get(owner=self.request.user)
            return Event.objects.filter(venue=venue)
        except Venue.DoesNotExist:
            staff = VenueStaffMember.objects.get(user=self.request.user)
            return Event.objects.filter(venue=staff.venue)

class UpdateEventView(LoginRequiredMixin, SuccessMessageMixin, UserHasPermissionMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_message = "Event Updated successfully"
    success_url = reverse_lazy("events")
    template_name = "event/update_event.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            staff = VenueStaffMember.objects.get(user=self.request.user)
            if staff.user_id != instance.event_manager_id:
                raise PermissionDenied("Only venue owner or event manager is allowed to edit this event!")
            else:
                instance.save()
        except VenueStaffMember.DoesNotExist:
            instance.save()
        return super().form_valid(form)
        
class DeleteEventView(LoginRequiredMixin, SuccessMessageMixin, UserHasPermissionMixin, DeleteView):
    model = Event
    success_message = "Event Delete Successfull"
    success_url = reverse_lazy("events")
    template_name = "venue/venue_confirm_delete.html"
    

    
        
