from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
     path("events/",EventView.as_view(),name="view_event"),
     path("venue_list/", VenueListView.as_view(), name="venue-list"),
    
    # ------------- Authenticate Section --------------------------
    path("registration/", UserCreationView.as_view(), name="registration"),
    path("log_in/", UserLoginView.as_view(), name="log-in"),
    path("log_out/", auth_views.LogoutView.as_view(), name="log-out"),
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
    path("list_events/",EventListView.as_view(),name="events"),
    path("event_detail/<int:pk>",EventDetailView.as_view(),name="event-detail"),
    path("update_event/<int:pk>",UpdateEventView.as_view(), name="update-event"),
    path("delete_event/<int:pk>",DeleteEventView.as_view(), name="delete-event"),
    
    # --------------- Ticket Section ----------------------- 
    path("create_ticket/",CreateTicketView.as_view(),name="create-ticket"),
    path("book_event/",BookEventView.as_view(),name="book-ticket"),
    path("cancel_booking/<int:id>",CancelBookingView.as_view(),name="cancel-booking"),
    
    # ---------------- Password Reset Section -------------------
    path("password_reset/",auth_views.PasswordResetView.as_view(),name="password_reset"),
    path("password_reset_done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path("password_reset_confrim/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    
]
