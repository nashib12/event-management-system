from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
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

# class VenueStaff(models.Model):
#     venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="venue_staffs")
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     is_venue_staff = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    
#     class Meta:
#         db_table = 'Venue Staffs'
#         managed = True


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
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING, related_name="event_type", default="")
    event_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.event_name
    
    class Meta:
        db_table = 'Events'
        managed = True
        ordering = ['-created_at']
    