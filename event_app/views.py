from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages

from .forms import *
from .models import *
from .mixins import *
from .validators import password_validate

class HomeView(TemplateView):
    template_name = "event_app/index.html"
    
class EventView(ListView):
    model = Event
    context_object_name = "events"
    template_name = "event_app/event.html"
    
    def get_queryset(self):
        return Event.objects.all().prefetch_related("tickets")

class VenueListView(ListView):
    model = Venue
    context_object_name = "venues"
    template_name = "event_app/venue.html"

#------------------- Authentication section -------------------------
class UserCreationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "authenticate/registration.html"
    success_url = reverse_lazy("create-profile")
    
    def form_valid(self, form):
        password = form.cleaned_data['password1']
        try:
            password_validate(password)
            user = super().form_valid(form)
            login(self.request, self.object)
            return  user
        except ValidationError as e:
            messages.error(self.request, str(e))
            return super().form_invalid(form)
    
class ProfileCreationView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "authenticate/create_profile.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
        password = form.cleaned_data['password1']
        password_validate(password)
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
    
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = "events"
    template_name = "event/event_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user
        
        has_bookking = event.get_user_booking(user)
        context.update({
            'has_booking' : has_bookking is not None,
        })
        return context
    
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
    
# ---------------------------- Ticket Section --------------------------------
class CreateTicketView(LoginRequiredMixin, SuccessMessageMixin, UserHasPermissionMixin, CreateView):
    model = TotalTickets
    form_class = TicketForm
    success_message = "Ticket Create Successfully"
    template_name = "tickets/create_ticket.html"
    success_url = reverse_lazy("events")
    
    def form_valid(self, form):
        event_id = self.request.GET.get("event_id")
        instance = form.save(commit=False)
        instance.event_id = event_id
        instance.save()
        return super().form_valid(form)

class BookEventView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BookEvent
    form_class = BookingForm
    success_message = "Event Booked Successfully"
    template_name = "tickets/book_event.html"
    success_url = reverse_lazy("view_event")
    
    def form_valid(self, form):
        tickets = form.cleaned_data["booked_ticekts"]
        event_id = self.request.GET.get("event_id")
        instance = form.save(commit=False)
        instance.booked_event_id = event_id
        instance.booked_by = self.request.user
        instance.save()
        sold_ticjets = TotalTickets.objects.get(event_id=event_id)
        sold_ticjets.sold_tickets = sold_ticjets.sold_tickets + tickets
        sold_ticjets.save()
        return super().form_valid(form)
    
class CancelBookingView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BookEvent
    success_url = reverse_lazy("view_event")
    success_message = "Booking cancelled successfully!"
    template_name = "tickets/cancel_booking.html"
    
    def get_object(self, queryset=None):
        event_id = self.kwargs.get('id') 
        return get_object_or_404(BookEvent, booked_event_id=event_id, booked_by=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        event_id = booking.booked_event_id
        
        # Update ticket count
        tickets = get_object_or_404(TotalTickets, event_id=event_id)
        tickets.sold_tickets = tickets.sold_tickets - booking.booked_tickets
        tickets.save()
        
        # Delete the booking
        return super().delete(request, *args, **kwargs)
    
