from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from calendar import month_name
from phonenumber_field.formfields import PhoneNumberField

from .validators import password_validate, email_validate
from .models import Profile, Venue, Event

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['class'] = ''
        self.fields['username'].widget.attrs['placeholder'] = ''
        
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['class'] = ''
        self.fields['password1'].widget.attrs['placeholder'] = ''
        
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['class'] = ''
        self.fields['password2'].widget.attrs['placeholder'] = ''
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        password_validate(password)
        return
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_validate(email)
        return

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('contact', 'profile_pic', 'address', 'birth_year', 'birth_month', 'birth_day', 'is_venue_owner')
        
        labels = {
            'conatct' : '',
            'profile_pic' : '',
            'address' : '',
            'birth_year' : '',
            'birth_month' : '',
            'birth_day' : '',
            'is_venue_owner' : '',
        }

        widgets = {
            'conatct' : forms.TextInput(attrs={}),
            'profile_pic' : forms.FileInput(attrs={}),
            'address' : forms.TextInput(attrs={}),
            'birth_year' : forms.Select(choices=['', 'Year'] + [(y, y) for y in range(1900, datetime.now().year + 1)], attrs={}),
            'birth_month' : forms.Select(choices=['', 'Month'] + [(m, month_name[m]) for m in range(1, 13)], attrs={}),
            'birth_day' : forms.Select(choices=['', 'Day'] + [(d, d) for d in range(1, 32)], attrs={}),
            'is_venue_owner' : forms.CheckboxInput(attrs={}),
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('venue_name', 'venue_address', 'venue_contact', 'venue_email', 'venue_website', 'venue_type')
        
        labels = {
            'venue_name': '', 
            'venue_address' : '', 
            'venue_contact' : '', 
            'venue_email' : '', 
            'venue_website' : '', 
            'venue_type' : '',
        }
        
        widgets = {
            'venue_name' : forms.TextInput(attrs={}), 
            'venue_address' : forms.TextInput(attrs={}), 
            'venue_contact' : forms.TextInput(attrs={}), 
            'venue_email' : forms.EmailInput(attrs={}), 
            'venue_website' : forms.URLInput(attrs={}), 
            'venue_type' : forms.Select(attrs={}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =  ('event_name', 'event_year', 'event_month', 'event_day', 'event_time', 'event_poster', 'event_manager', 'event_description')        

        labels = {
            'event_name' : '', 
            'event_year' : '', 
            'event_month' : '', 
            'event_day' : '', 
            'event_time' : '', 
            'event_poster' : '', 
            'event_manager' : '', 
            'event_description' : '',
        }
        
        widgets = {
            'event_name' : forms.TextInput(attrs={}), 
            'event_year' : forms.Select(choices=['', 'Year'] + [(y, y) for y in range(1900, datetime.now().year + 1)], attrs={}),
            'event_month' : forms.Select(choices=['', 'Month'] + [(m, month_name[m]) for m in range(1, 13)], attrs={}),
            'event_day' : forms.Select(choices=['', 'Day'] + [(d, d) for d in range(1, 32)], attrs={}), 
            'event_time' : forms.TimeInput(attrs={}), 
            'event_poster' : forms.FileInput(attrs={}), 
            'event_manager' : forms.Select(attrs={}), 
            'event_description' : forms.Textarea(attrs={}),
        }
