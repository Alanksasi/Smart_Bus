from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from app_operator.models import BusRoutes, LiveLocation, Seats, Trip
from app_passenger.models import Booking
from app_dashboard.models import Passenger
from app_core import models

# Create your views here.

def bview(request,name):
    view = BusRoutes.objects.filter(rid=name)            
    return render(request,"bview.html",{"bview":view})

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid
#     seats = Seats.objects.filter(bid=bus)
#     booked = Booking.objects.filter(trip=trip).values_list('seat_id', flat=True)

#     return render(request, "passenger/seats.html", {
#         "bus": bus,
#         "seats": seats,
#         "booked": booked
#     })

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid

#     seats = Seats.objects.filter(bid=bus)

#     booked = Booking.objects.filter(trip=trip).values_list('seat_id', flat=True)

#     return render(request, "passenger/seats.html", {
#         "bus": bus,
#         "seats": seats,
#         "booked": booked
#     })

# def book(request, trip_id, seat_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     seat = get_object_or_404(Seats, id=seat_id)
#     passenger = Passenger.objects.get(user=request.user)

#     if Booking.objects.filter(trip=trip, seat=seat).exists():
#         messages.error(request, "Seat already booked")
#     else:
#         Booking.objects.create(
#             passenger=passenger,
#             trip=trip,
#             seat=seat
#         )

#     return redirect("passenger:mybookings")

# def book(request, trip_id, seat_id):
#     trip = Trip.objects.get(id=trip_id)
#     seat = Seats.objects.get(id=seat_id)
#     passenger = Passenger.objects.get(user=request.user)

#     if Booking.objects.filter(trip=trip, seat=seat).exists():
#         messages.error(request, "Seat already booked")
#         return redirect('passenger:seats', trip_id)

#     Booking.objects.create(
#         passenger=passenger,
#         trip=trip,
#         seat=seat,
#         payment_status="pending"
#     )

#     return redirect('passenger:payment', trip_id=trip.id)

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid

#     seats = Seats.objects.filter(bid=bus)

#     booked = Booking.objects.filter(trip=trip).values_list('seat_id', flat=True)

#     return render(request, "passenger/seats.html", {
#         "bus": bus,
#         "seats": seats,
#         "booked": booked
#     })

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid

#     # All seats of that bus
#     seats = Seats.objects.filter(bid=bus).order_by('seatno')

#     # Already booked seats for that trip
#     booked_seats = Booking.objects.filter(
#         trip=trip
#     ).values_list('seat_id', flat=True)

#     return render(request, "passenger/seats.html", {
#         "trip": trip,
#         "bus": bus,
#         "seats": seats,
#         "booked_seats": booked_seats
#     })

def seats(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    bus = trip.busroute.bid

    seats = Seats.objects.filter(bid=bus)

    booked = Booking.objects.filter(
        trip=trip
    ).values_list('seat_id', flat=True)

    return render(request, "passenger/seats.html", {
        "trip": trip,
        "bus": bus,
        "seats": seats,
        "booked": booked
    })

# def book_seat(request, trip_id, seat_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     seat = get_object_or_404(Seats, id=seat_id)
#     passenger = Passenger.objects.get(user=request.user)

#     if Booking.objects.filter(trip=trip, seat=seat).exists():
#         messages.error(request, "Seat already booked")
#     else:
#         Booking.objects.create(
#             passenger=passenger,
#             trip=trip,
#             seat=seat
#         )

#     return redirect("passenger:mybookings")

def book_seat(request, trip_id, seat_id):
    trip = Trip.objects.get(id=trip_id)
    seat = Seats.objects.get(id=seat_id)
    passenger = Passenger.objects.get(user=request.user)

    if Booking.objects.filter(trip=trip, seat=seat).exists():
        messages.error(request, "Seat already booked")
        return redirect('passenger:seats', trip_id)

    Booking.objects.create(
        passenger=passenger,
        trip=trip,
        seat=seat,
        payment_status="pending"
    )

    return redirect('passenger:payment', trip_id=trip.id)  
 
def track(request, trip_id):
    location = LiveLocation.objects.get(trip_id=trip_id)
    return render(request, "passenger/track.html", {"location": location})

def payment(request, trip_id):
    bookings = Booking.objects.filter(
        trip_id=trip_id,
        passenger__user=request.user,
        payment_status="pending"
    )

    if request.method == "POST":
        bookings.update(payment_status="paid")
        return redirect('passenger:mybookings')

    return render(request, "passenger/payment.html", {
        "bookings": bookings
    })
