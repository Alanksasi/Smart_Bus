# from pyexpat.errors import messages
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.utils.timezone import now

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
    bus_routes = BusRoutes.objects.filter(rid=name)
    today = date.today()

    buses_with_trips = []

    for br in bus_routes:
        trip = Trip.objects.filter(
            busroute=br,
            date__gte=today,   # future + today only
            status__in=['scheduled', 'running']  # only active trips
        ).order_by('date').first()

        if trip:   # Only append if trip exists
            buses_with_trips.append({
                'bus_route': br,
                'trip': trip
            })

    return render(request, "bview.html", {
        "buses": buses_with_trips
    })
    
# def bview(request, name):
#     # 'name' is the route ID (rid)
#     bus_routes = BusRoutes.objects.filter(rid=name)
#     today = date.today()
    
#     buses_with_trips = []
#     for br in bus_routes:
#         # Find trip for today
#         # We could also filter by status='scheduled' or 'running'
#         trip = Trip.objects.filter(busroute=br, date=today).first()
#         buses_with_trips.append({
#             'bus_route': br,
#             'trip': trip
#         })
            
#     return render(request,"bview.html",{"buses": buses_with_trips})

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

# def seats(request, trip_id):
#     trip = Trip.objects.get(id=trip_id)
#     bus = trip.busroute.bid

#     seats = Seats.objects.filter(bid=bus).order_by('seatno')

#     # booked = Booking.objects.filter(
#     #     trip=trip
#     # ).values_list('seat_id', flat=True)
    
#     # Updated for BookingDetails
#     # We need to find all BookingDetails related to this trip
#     # BookingDetails -> BookingMaster -> Trip
#     booked = BookingDetails.objects.filter(
#         master__trip=trip
#     ).values_list('seat_id', flat=True)

#     return render(request, "seats.html", {
#         "trip": trip,
#         "bus": bus,
#         "seats": seats,
#         "booked_seats": booked
#     })

def seats(request, trip_id):
    trip = get_object_or_404(
        Trip,
        id=trip_id,
        date__gte=date.today(),
        status__in=['scheduled', 'running']
    )

    bus = trip.busroute.bid

    seats = Seats.objects.filter(bid=bus).order_by('seatno')

    booked = BookingDetails.objects.filter(
        master__trip=trip
    ).values_list('seat_id', flat=True)

    return render(request, "seats.html", {
        "trip": trip,
        "bus": bus,
        "seats": seats,
        "booked_seats": booked
    })
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

def bview(request, name):
    bus_routes = BusRoutes.objects.filter(rid=name)
    today = date.today()

    buses_with_trips = []

    for br in bus_routes:
        trip = Trip.objects.filter(
            busroute=br,
            date__gte=today,   # future + today only
            status__in=['scheduled', 'running']  # only active trips
        ).order_by('date').first()

        if trip:   # Only append if trip exists
            buses_with_trips.append({
                'bus_route': br,
                'trip': trip
            })

    return render(request, "bview.html", {
        "buses": buses_with_trips
    })

# def book_seats(request, trip_id):
#     if request.method != "POST":
#         return redirect('passenger:routes')

#     seat_ids = request.POST.getlist('seats')

#     trip = get_object_or_404(
#         Trip,
#         id=trip_id,
#         date__gte=date.today(),
#         status__in=['scheduled', 'running']
#     )

#     passenger = Passenger.objects.filter(user=request.user).first()
#     if not passenger:
#         messages.error(request, "Passenger profile not found.")
#         return redirect('passenger:routes')

#     if not seat_ids:
#         messages.error(request, "No seats selected!")
#         return redirect('passenger:seats', trip_id=trip_id)

#     # Validate seats belong to this bus
#     selected_seats = Seats.objects.filter(
#         id__in=seat_ids,
#         bus=trip.busroute.bid   # Adjust based on your model relation
#     )

#     if selected_seats.count() != len(seat_ids):
#         messages.error(request, "Invalid seat selection.")
#         return redirect('passenger:seats', trip_id=trip_id)

#     with transaction.atomic():

#         # Lock rows to prevent double booking
#         already_booked = BookingDetails.objects.select_for_update().filter(
#             master__trip=trip,
#             seat_id__in=seat_ids
#         ).exists()

#         if already_booked:
#             messages.error(request, "One or more seats already booked.")
#             return redirect('passenger:seats', trip_id=trip_id)

#         # Calculate total price safely
#         total_price = selected_seats.aggregate(
#             total=sum('seat_price')
#         )['total'] or 0

#         # Create BookingMaster
#         master = BookingMaster.objects.create(
#             passenger=passenger,
#             trip=trip,
#             amount=total_price,
#             payment_status="pending"
#         )

#         # Create BookingDetails
#         BookingDetails.objects.bulk_create([
#             BookingDetails(master=master, seat=seat)
#             for seat in selected_seats
#         ])

#     return redirect('passenger:payment', trip_id=master.id)

def book_seats(request, trip_id):
    if request.method != "POST":
        return redirect('passenger:routes')

    seat_ids = request.POST.getlist('seats')

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        date__gte=date.today(),
        status__in=['scheduled', 'running']
    )

    passenger = Passenger.objects.filter(user=request.user).first()
    if not passenger:
        messages.error(request, "Passenger profile not found.")
        return redirect('passenger:routes')

    if not seat_ids:
        messages.error(request, "No seats selected!")
        return redirect('passenger:seats', trip_id=trip_id)

    # ✅ FIXED HERE
    selected_seats = Seats.objects.filter(
        id__in=seat_ids,
        bid=trip.busroute.bid
    )

    if selected_seats.count() != len(seat_ids):
        messages.error(request, "Invalid seat selection.")
        return redirect('passenger:seats', trip_id=trip_id)

    with transaction.atomic():

        already_booked = BookingDetails.objects.select_for_update().filter(
            master__trip=trip,
            seat_id__in=seat_ids
        ).exists()

        if already_booked:
            messages.error(request, "One or more seats already booked.")
            return redirect('passenger:seats', trip_id=trip_id)

        # ✅ FIXED HERE
        total_price = selected_seats.aggregate(
            total=Sum('seat_price')
        )['total'] or 0

        master = BookingMaster.objects.create(
            passenger=passenger,
            trip=trip,
            amount=total_price,
            payment_status="pending"
        )

        BookingDetails.objects.bulk_create([
            BookingDetails(master=master, seat=seat)
            for seat in selected_seats
        ])

    return redirect('passenger:payment', trip_id=master.id)

# def book_seats(request, trip_id):
#     if request.method == "POST":
#         seat_ids = request.POST.getlist('seats')
#         trip = get_object_or_404(
#             Trip,
#             id=trip_id,
#             date__gte=date.today(),
#             status__in=['scheduled', 'running']
#         )
#         # trip = get_object_or_404(Trip, id=trip_id)
#         passenger = Passenger.objects.filter(user=request.user).first()

#         if not passenger:
#             messages.error(request, "Passenger profile not found.")
#             return redirect('passenger:routes')

#         if not seat_ids:
#             messages.error(request, "No seats selected!")
#             return redirect('passenger:seats', trip_id=trip_id)

#         # Check availability
#         already_booked = BookingDetails.objects.filter(master__trip=trip, seat_id__in=seat_ids).exists()
#         if already_booked:
#             messages.error(request, "One or more selected seats are already booked.")
#             return redirect('passenger:seats', trip_id=trip_id)

#         # Calculate amount
#         total_price = 0
#         selected_seats = Seats.objects.filter(id__in=seat_ids)
#         for s in selected_seats:
#             total_price += s.seat_price

#         # Create Master
#         master = BookingMaster.objects.create(
#             passenger=passenger,
#             trip=trip,
#             amount=total_price,
#             payment_status="pending"
#         )

#         # Create Details
#         details = []
#         for seat in selected_seats:
#             details.append(BookingDetails(
#                 master=master,
#                 seat=seat
#             ))
#         BookingDetails.objects.bulk_create(details)

#         return redirect('passenger:payment', trip_id=master.id)
    
#     return redirect('passenger:routes')  
 

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

# def track(request, trip_id):
#     location = LiveLocation.objects.get(trip_id=trip_id)
#     return render(request, "track.html", {"location": location})

def track(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    try:
        location = LiveLocation.objects.get(trip=trip)
    except LiveLocation.DoesNotExist:
        location = None

    return render(request, "track.html", {
        "trip": trip,
        "location": location
    })


def today_trips(request):
    today = now().date()

    bookings = BookingMaster.objects.filter(
        passenger__user=request.user,
        trip__date=today,
        # payment_status="paid"   # optional but recommended
    ).select_related("trip", "trip__busroute__bid")

    return render(request, "today_trips.html", {
        "bookings": bookings
    })