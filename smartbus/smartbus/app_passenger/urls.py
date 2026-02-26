from django.urls import path
from app_passenger import views


app_name="passenger"
urlpatterns = [
    path("routes/", views.routes, name="routes"),
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
    # Book multiple seats
    path("book_seats/<int:trip_id>/", views.book_seats, name="book_seats"),

    path("mybookings/", views.mybookings, name="mybookings"),
    
    # Payment
    path("payment/<int:trip_id>/", views.payment, name="payment"),

    # NEW — live bus tracking
    path("track/<int:trip_id>/", views.track, name="track"),
    
]