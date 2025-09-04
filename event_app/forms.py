from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from calendar import month_name
from django.contrib.auth.forms import AuthenticationForm
# from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .validators import password_validate
from .models import Profile, Venue, Event

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control fs-4','id':'fname'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control fs-4','id':'lname'}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class':'form-control fs-4','id':'email'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['username'].widget.attrs['id'] = 'username'
        
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['password1'].widget.attrs['placeholder'] = ''
        self.fields['password1'].widget.attrs['id'] = 'password1'
        
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control fs-4'
        self.fields['password2'].widget.attrs['placeholder'] = ''
        self.fields['password2'].widget.attrs['id'] = 'password2'
        
    
class ProfileForm(forms.ModelForm):
    # contact = forms.CharField(widgets = PhoneNumberPrefixWidget(attrs={'id': 'phone','class': 'form-control'}),)
        
    class Meta:
        model = Profile
        fields = ('contact', 'profile_pic', 'address', 'birth_year', 'birth_month', 'birth_day', 'is_venue_owner')
        
        labels = {
            'contact' : '',
            'profile_pic' : '',
            'address' : '',
            'birth_year' : '',
            'birth_month' : '',
            'birth_day' : '',
            'is_venue_owner' : '',
        }

        widgets = {
            'contact' : forms.TextInput(attrs={'class':'form-control fs-4','id':'contact'}),
            'profile_pic' : forms.FileInput(attrs={'class':'form-control fs-4','id':'profile_pic'}),
            'address' : forms.TextInput(attrs={'class':'form-control fs-4','id':'address'}),
            'birth_year' : forms.Select(choices=[('', 'Year')] + [(y, y) for y in range(1900, datetime.now().year + 1)], attrs={'class':'form-control fs-4','id':'year'}),
            'birth_month' : forms.Select(choices=[('', 'Month')] + [(m, month_name[m]) for m in range(1, 13)], attrs={'class':'form-control fs-4','id':'month'}),
            'birth_day' : forms.Select(choices=[('', 'Day')] + [(d, d) for d in range(1, 32)], attrs={'class':'form-control fs-4','id':'day'}),
            'is_venue_owner' : forms.CheckboxInput(attrs={'class':'form-check-input fs-4','id':'owner', 'type' : 'checkbox'}),
        }

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'venue_address', 'venue_contact', 'venue_email', 'venue_website', 'venue_type']
        
        labels = {
            'venue_name': '', 
            'venue_address' : '', 
            'venue_contact' : '', 
            'venue_email' : '', 
            'venue_website' : '', 
            'venue_type' : '',
        }
        
        widgets = {
            'venue_name' : forms.TextInput(attrs={'class':'form-control fs-4','id':'name'}), 
            'venue_address' : forms.TextInput(attrs={'class':'form-control fs-4','id':'address'}), 
            'venue_contact' : forms.TextInput(attrs={'class':'form-control fs-4','id':'contact'}), 
            'venue_email' : forms.EmailInput(attrs={'class':'form-control fs-4','id':'email'}), 
            'venue_website' : forms.URLInput(attrs={'class':'form-control fs-4','id':'website'}), 
            'venue_type' : forms.Select(attrs={'class':'form-control fs-4','id':'venue_type'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =  ['event_name', 'event_year', 'event_month', 'event_day', 'event_time', 'event_poster', 'event_manager', 'event_description']        

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
            'event_name' : forms.TextInput(attrs={'class':'form-control fs-4','id':'name'}), 
            'event_year' : forms.Select(choices=[('', 'Year')] + [(y, y) for y in range(1900, datetime.now().year + 1)], attrs={'class':'form-control fs-4','id':'year'}),
            'event_month' : forms.Select(choices=[('', 'Month')] + [(m, month_name[m]) for m in range(1, 13)], attrs={'class':'form-control fs-4','id':'month'}),
            'event_day' : forms.Select(choices=[('', 'Day')] + [(d, d) for d in range(1, 32)], attrs={'class':'form-control fs-4','id':'day'}), 
            'event_time' : forms.TimeInput(attrs={'class':'form-control fs-4','id':'etime'}), 
            'event_poster' : forms.FileInput(attrs={'class':'form-control fs-4','id':'poster'}), 
            'event_manager' : forms.Select(attrs={'class':'form-control fs-4','id':'manager'}), 
            'event_description' : forms.Textarea(attrs={'class':'form-control fs-4','id':'description'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class' : 'form-control fs-4', 'id' : 'username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class' : 'form-control fs-4', 'id' : 'password'}))