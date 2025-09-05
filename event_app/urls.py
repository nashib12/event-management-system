from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # ------------- Authenticate Section --------------------------
    path("registration/", UserCreationView.as_view(), name="registration"),
    path("log_in/", UserLoginView.as_view(), name="log-in"),
    path("log_out/", LogoutView.as_view(), name="log-out"),
    path("profile_create/",ProfileCreationView.as_view(),name="create-profile"),
    path("update_profile/<int:pk>", ProfileUpdateView.as_view(),name="update-profile"),
    path("change_password/", UserPasswordChangeView.as_view(),name="change-password"),
    
    # ---------------------- Venue Section --------------------
    path("venue_create/",VenueCreationView.as_view(),name="create-venue"),
    path("update_venue/<int:pk>",UpdateVenueView.as_view(), name="update-venue"),
    path("delete_venue/<int:pk>",VenueDeleteView.as_view(), name="delete-venue"),
    path("venue/",VenueView.as_view(),name="view-venue"),
    path("venue_staff_create/",VenueStaffCreateView.as_view(),name="create-venue-staff"),
    
    # ------------------------ Event Section -------------------------------
    path("event_create/",EventCreationView.as_view(),name="create-event"),
    path("events/",EventListView.as_view(),name="events"),
    path("update_event/<int:pk>",UpdateEventView.as_view(), name="update-event"),
    path("delete_event/<int:pk>",DeleteEventView.as_view(), name="delete-event"),
]
