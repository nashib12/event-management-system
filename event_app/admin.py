from django.contrib import admin

from .models import Profile, Venue, VenueStaff, VenueType, Event, EventType
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'is_venue_owner')
    ordering = ['-created_at']
    fields = ['user', 'ia_active', 'is_venue_owner']
    
admin.site.register([VenueType, EventType])

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('owner', 'venue_name', 'venue_type')
    ordering = ('-registered_at',)
    list_filters = ('venue_type', 'registered_at')
    fields = ['owner', 'venue_name', 'venue_type', 'is_approved']
    
@admin.register(VenueStaff)
class VenueStaffAdmin(admin.ModelAdmin):
    list_display = ('venue', 'first_name', 'last_name', 'is_active')
    ordering = ('-created_at',)
    list_filters = ('venue')
    fields = ['venue','is_active', 'is_venue_staff']
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('venue', 'event_name', 'event_year', 'event_month', 'event_day', 'event_manager')
    ordering = ('event_time',)
    list_filter = ('venue', 'event_day', 'event_month', 'event_year')
    fields = ['venue', 'event_name', ('event_year', 'event_month', 'event_day'), 'event_time', 'event_manager']
    
