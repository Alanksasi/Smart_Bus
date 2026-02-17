from django.urls import path
from app_passenger import views


app_name="passenger"
urlpatterns = [
    path("bview/<int:name>", views.bview, name="bview"),
    
    # # NEW — seat layout for booking
    # path("seats/<int:trip_id>/", views.seats, name="seats"),

    # # NEW — book seat
    # path("book/<int:trip_id>/<int:seat_id>/", views.book, name="book"),

    # NEW — passenger booking history (optional but recommended)
    # path("mybookings/", views.mybookings, name="mybookings"),

    # Seat layout page
    path("seats/<int:trip_id>/", views.seats, name="seats"),

    # Book a seat
    path("book_seat/<int:trip_id>/<int:seat_id>/", views.book_seat, name="book_seat"),
    
    # NEW — live bus tracking
    path("track/<int:trip_id>/", views.track, name="track"),
]