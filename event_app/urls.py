from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registration/", UserCreationView.as_view(), name="registration"),
    path("profile_create/",ProfileCreationView.as_view(),name="create-profile"),
    path("venue_create/",VenueCreationView.as_view(),name="create-venue"),
    path("event_create/",EventCreationView.as_view(),name="create-event"),
]
