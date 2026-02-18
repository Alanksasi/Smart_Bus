from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from app_operator.models import BusRoutes, LiveLocation, Seats, Trip, Routes
from app_passenger.models import BookingMaster, BookingDetails
from app_dashboard.models import Passenger
from app_core import models

# Create your views here.

# Create your views here.

from datetime import date

def routes(request):
    routes_list = Routes.objects.all()
    return render(request, "routes.html", {"routes": routes_list})

def bview(request, name):
    # 'name' is the route ID (rid)
    bus_routes = BusRoutes.objects.filter(rid=name)
    today = date.today()
    
    buses_with_trips = []
    for br in bus_routes:
        # Find trip for today
        # We could also filter by status='scheduled' or 'running'
        trip = Trip.objects.filter(busroute=br, date=today).first()
        buses_with_trips.append({
            'bus_route': br,
            'trip': trip
        })
            
    return render(request,"bview.html",{"buses": buses_with_trips})

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid
#     seats = Seats.objects.filter(bid=bus)
#     booked = Booking.objects.filter(trip=trip).values_list('seat_id', flat=True)

#     return render(request, "seats.html", {
#         "bus": bus,
#         "seats": seats,
#         "booked": booked
#     })

# def seats(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     bus = trip.busroute.bid

#     seats = Seats.objects.filter(bid=bus)

#     booked = Booking.objects.filter(trip=trip).values_list('seat_id', flat=True)

#     return render(request, "seats.html", {
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

#     return render(request, "seats.html", {
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

#     return render(request, "seats.html", {
#         "trip": trip,
#         "bus": bus,
#         "seats": seats,
#         "booked_seats": booked_seats
#     })

def seats(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    bus = trip.busroute.bid

    seats = Seats.objects.filter(bid=bus).order_by('seatno')

    # booked = Booking.objects.filter(
    #     trip=trip
    # ).values_list('seat_id', flat=True)
    
    # Updated for BookingDetails
    # We need to find all BookingDetails related to this trip
    # BookingDetails -> BookingMaster -> Trip
    booked = BookingDetails.objects.filter(
        master__trip=trip
    ).values_list('seat_id', flat=True)

    return render(request, "seats.html", {
        "trip": trip,
        "bus": bus,
        "seats": seats,
        "booked_seats": booked
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

def book_seats(request, trip_id):
    if request.method == "POST":
        seat_ids = request.POST.getlist('seats')
        trip = get_object_or_404(Trip, id=trip_id)
        passenger = Passenger.objects.filter(user=request.user).first()

        if not passenger:
            messages.error(request, "Passenger profile not found.")
            return redirect('passenger:routes')

        if not seat_ids:
            messages.error(request, "No seats selected!")
            return redirect('passenger:seats', trip_id=trip_id)

        # Check availability
        already_booked = BookingDetails.objects.filter(master__trip=trip, seat_id__in=seat_ids).exists()
        if already_booked:
            messages.error(request, "One or more selected seats are already booked.")
            return redirect('passenger:seats', trip_id=trip_id)

        # Calculate amount
        total_price = 0
        selected_seats = Seats.objects.filter(id__in=seat_ids)
        for s in selected_seats:
            total_price += s.seat_price

        # Create Master
        master = BookingMaster.objects.create(
            passenger=passenger,
            trip=trip,
            amount=total_price,
            payment_status="pending"
        )

        # Create Details
        details = []
        for seat in selected_seats:
            details.append(BookingDetails(
                master=master,
                seat=seat
            ))
        BookingDetails.objects.bulk_create(details)

        return redirect('passenger:payment', trip_id=master.id)
    
    return redirect('passenger:routes')  
 
def track(request, trip_id):
    location = LiveLocation.objects.get(trip_id=trip_id)
    return render(request, "track.html", {"location": location})

def payment(request, trip_id):
    # trip_id is treated as booking_master_id here
    booking_id = trip_id 
    booking = get_object_or_404(BookingMaster, id=booking_id, passenger__user=request.user)

    if request.method == "POST":
        booking.payment_status = "paid"
        booking.save()
        return redirect('passenger:mybookings')

    return render(request, "payment.html", {
        "booking": booking
    })

def mybookings(request):
    passenger = Passenger.objects.filter(user=request.user).first()
    if not passenger:
        # Handle case where user is not a passenger
        return redirect('passenger:routes')
        
    bookings = BookingMaster.objects.filter(passenger=passenger).order_by('-booked_at')
    return render(request, "mybookings.html", {"bookings": bookings})
