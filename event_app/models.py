from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="users")
    contact = PhoneNumberField()
    profile_pic = models.ImageField(upload_to="profile/", default="profile/default_profile.jpg")
    address = models.CharField(max_length=200)
    birth_day = models.IntegerField()
    birth_month = models.IntegerField()
    birth_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_venue_owner = models.BooleanField(default=False)
    ia_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'User Profile'
        managed = True
        ordering = ['-created_at']

class VenueType(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Venue Type'
        managed = True

class Venue(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owners")
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=200)
    venue_contact = PhoneNumberField()
    venue_email = models.EmailField(unique=True)
    venue_website = models.URLField(blank=True, null=True)
    venue_type = models.ForeignKey(VenueType, on_delete=models.DO_NOTHING, related_name="venues_type")
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.venue_name
    
    class Meta:
        db_table = 'Venues'
        managed = True
        
class VenueStaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user", primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue_staffs")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_venue_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'Venue Staff Members'
        managed = True
    
class EventType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Event Types'
        managed = True

class Event(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="events")
    event_name = models.CharField(max_length=200)
    event_day = models.IntegerField()
    event_month = models.IntegerField()
    event_year = models.IntegerField()
    event_time = models.TimeField()
    event_poster = models.ImageField(upload_to="event_poster/")
    event_manager = models.ForeignKey(VenueStaffMember, on_delete=models.DO_NOTHING, related_name="managers")
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING, related_name="event_type", default="", null=True)
    event_description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.event_name
    
    class Meta:
        db_table = 'Events'
        managed = True
        ordering = ['-created_at']
    
    def get_user_booking(self, user):
        try:
            return self.bookings.get(booked_by=user, status='booked')
        except BookEvent.DoesNotExist:
            return None
    
class TotalTickets(models.Model):
    event = models.OneToOneField(Event, primary_key=True, on_delete=models.CASCADE, related_name="tickets")
    total_tickets = models.PositiveIntegerField()
    sold_tickets = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def remaining_tickets(self):
        return max(0, self.total_tickets - self.sold_tickets)
    
    @property
    def is_sold_out(self):
        return self.remaining_tickets == 0
    
    @property
    def percentage_sold(self):
        if self.total_tickets == 0:
            return 0
        return (self.sold_tickets / self.total_tickets) * 100

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.event} ({self.remaining_tickets} remaining)"
    
    class Meta:
        db_table = 'Event Ticket'
        managed = True
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at']

class BookEvent(models.Model):
    booked_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booked_ticekts = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')], default="booked")
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Booking'
        managed = True
        unique_together = ("booked_by", "booked_event")