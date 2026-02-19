from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from app_operator.models import BusReg, BusRoutes, LiveLocation, Routes, Seats, Trip
from app_passenger.models import BookingMaster, BookingDetails
from app_core.models import Location

from django.contrib.auth.decorators import login_required

# Create your views here.
#------------------------------------------------Bus Registration(done by operator)------------------------------------------------
# def generate_seats(bus):
#     rows = bus.total_rows

#     if bus.seat_type == '2x2':
#         cols = ['A', 'B', 'C', 'D']
#     # else:
#     elif bus.seat_type == '2x3':
#         cols = ['A', 'B', 'C', 'D', 'E']

#     for r in range(1, rows + 1):
#         for c in cols:
#             Seats.objects.create(
#                 bid=bus,
#                 seatno=f"{r}{c}"
#             )

def generate_seats(bus):
    if Seats.objects.filter(bid=bus).exists():
        return

    rows = bus.total_rows

    if bus.seat_type == '2x2':
        cols = ['A', 'B', 'C', 'D']
    else:
        cols = ['A', 'B', 'C', 'D', 'E']

    for r in range(1, rows + 1):
        for c in cols:
            Seats.objects.create(
                bid=bus,
                seatno=f"{r}{c}"
            )

@login_required
def busreg(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        num = request.POST.get("num", "").strip()
        con = request.POST.get("contact", "").strip()
        seat_type = request.POST.get("seat_type")
        total_rows = request.POST.get("total_rows")

        # Bus number duplicate check
        if BusReg.objects.filter(num=num).exists():
            return HttpResponse(
                "<script>alert('Bus already exists');"
                "window.location='/operator/busreg/';</script>"
            )

        # Create bus
        bus = BusReg.objects.create(
            name=name,
            num=num,
            con=con,
            seat_type=seat_type,
            total_rows=int(total_rows),
            user=request.user
        )

        # ⭐ Automatically generate seats
        generate_seats(bus)

        return HttpResponse(
            "<script>alert('Bus registered successfully');window.location='/operator/busreg/';</script>"
        )

    return render(request, "busregister.html")
# def busreg(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         num = request.POST.get("num")
#         con = request.POST.get("contact")
#         seat_type = request.POST.get("seat_type")
#         total_rows = request.POST.get("total_rows")

#         if BusReg.objects.filter(num=num).exists():
#             return HttpResponse("<script>alert('Bus already exists');window.location='/operator/busreg/';</script>")
#             # messages.error(request, "Bus already exists")
#             # return redirect("operator:busreg")

#         BusReg.objects.create(
#             name=name,
#             num=num,
#             con=con,
#             seat_type=seat_type,
#             total_rows=int(total_rows),
#             user=request.user
#         )
#         return HttpResponse("<script>alert('Bus registered successfully');window.location='/operator/busreg/';</script>")
#         # messages.success(request, "Bus registered successfully")
#         # return redirect("operator:busreg")
#     return render(request, "busregister.html")
    
#------------------------------------------------Bus view------------------------------------------------
def busv(request):
    view = BusReg.objects.filter(user=request.user)
    return render(request,"busview.html",{"busv":view})

#------------------------------------------------Bus Delete------------------------------------------------
def busdl(request,name):
    d = BusReg.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/operator/busv/';</script>")

#------------------------------------------------Bus Edit------------------------------------------------
def busup(request,name):
    up = BusReg.objects.get(id=name)
    if request.method=="POST":
        name = request.POST.get('name')
        num = request.POST.get('num')
        con = request.POST.get('contact')
        if BusReg.objects.filter(name = name, num = num).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/operator/busv/';</script>")
        up.name =name
        up.num = num
        up.con=con
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/operator/busv/';</script>")
    return render(request,"busedit.html", {"busv":up})

#------------------------------------------------Route Creation------------------------------------------------
def route(request):
    if request.method=="POST":
        name = request.POST.get('name')
        if Routes.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/operator/route/';</script>")
        r = Routes()
        r.name = name
        r.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/operator/route/';</script>")
    else:
        return render(request, "route.html")
    
#------------------------------------------------Route View------------------------------------------------
def routev(request):
    view = Routes.objects.all()
    return render(request,"routeview.html",{"routev":view})

#------------------------------------------------Route Delete------------------------------------------------
def routedl(request,name):
    d = Routes.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/operator/routev/';</script>")

#------------------------------------------------Route Update------------------------------------------------
def routeup(request,name):
    up = Routes.objects.get(id=name)
    if request.method=="POST":
        name = request.POST.get('name')
        if Routes.objects.filter(name =name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/operator/routev/';</script>")
        up.name=name
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/operator/routev/';</script>")
    return render(request,"routedit.html",{"routev":up})

#------------------------------------------------Bus Route Register------------------------------------------------ 
def busroute(request):
    if request.method=="POST":
        bid = request.POST.get('bid')
        rid = request.POST.get('rid')
        time = request.POST.get('time')
        if BusRoutes.objects.filter( bid=bid, rid=rid ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/operator/busroute/';</script>")
        r = BusRoutes()
        r.bid = BusReg.objects.get(id = bid)
        r.rid = Routes.objects.get(id = rid)
        r.time = time
        r.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/operator/busroute/';</script>")
    # else:
    v = Routes.objects.all()
    b = BusReg.objects.all()
    return render(request, "busroute.html", {"list":b , "lists":v})

#------------------------------------------------Bus Route View------------------------------------------------
def broutev(request):
    view = BusRoutes.objects.all()
    return render(request,"brouteview.html",{"broutev":view})

#------------------------------------------------Route Delete------------------------------------------------
def broutedl(request,name):
    d = BusRoutes.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/operator/broutev/';</script>")

def brouteup(request,name):
    up = BusRoutes.objects.get(id=name)
    if request.method=="POST":
        bid = request.POST.get('bid')
        rid = request.POST.get('rid')
        time = request.POST.get('time')
        if BusRoutes.objects.filter(bid=bid,rid=rid).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.bid=bid
        up.rid=rid
        up.time=time
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/operator/broutev/';</script>")
    return render(request,"busroutedit.html",{"broutev":up})

# def seats(request, bus_id):
#     bus = get_object_or_404(BusReg, id=bus_id)
#     rows = bus.total_rows

#     # Prevent regeneration
#     if Seats.objects.filter(bid=bus).exists():
#         return HttpResponse(
#             "<script>alert('Seats already generated');window.location='/operator/busv/';</script>"
#         )

#     # if Seats.objects.filter(bid=bus).exists():
#     #     messages.warning(request, "Seats already generated!")
#     #     return redirect('operator:busv')

#     if bus.seat_type == '2x2':
#         columns = ['A', 'B', 'C', 'D']
#         position_map = {
#             'A': 'window',
#             'B': 'aisle',
#             'C': 'aisle',
#             'D': 'window',
#         }

#     elif bus.seat_type == '2x3':
#         columns = ['A', 'B', 'C', 'D', 'E']
#         position_map = {
#             'A': 'window',
#             'B': 'aisle',
#             'C': 'middle',
#             'D': 'aisle',
#             'E': 'window',
#         }
#     else:
#         return HttpResponse(
#             "<script>alert('Invalid seat type');window.history.back();</script>"
#         )

#     # seat_list = []
#     # for row in range(1, rows + 1):
#     #     for col in columns:
#     #         seat_list.append(
#     #             Seats(
#     #                 bid=bus,
#     #                 seatno=f"{row}{col}",
#     #                 seat_price=742.00,  # dynamic later
#     #                 seat_position=position_map[col]
#     #             )
#     #         )
    
#     seat_list = [
#         Seats(
#             bid=bus,
#             seatno=f"{row}{col}",
#             seat_price=742.00,
#             seat_position=position_map[col]
#         )
#         for row in range(1, rows + 1)
#         for col in columns
#     ]

#     Seats.objects.bulk_create(seat_list)

#     return HttpResponse(
#         "<script>alert('Seats generated successfully');window.location='/operator/busv/';</script>"
#     )

def seats(request, bus_id):
    bus = get_object_or_404(BusReg, id=bus_id)
    rows = bus.total_rows

    # Prevent regeneration
    if Seats.objects.filter(bid=bus).exists():
        return HttpResponse(
            "<script>alert('Seats already generated!');"
            "window.location='/operator/busv/';</script>"
        )

    # Seat configuration
    if bus.seat_type == '2x2':
        columns = ['A', 'B', 'C', 'D']
        position_map = {
            'A': 'window',
            'B': 'aisle',
            'C': 'aisle',
            'D': 'window',
        }

    elif bus.seat_type == '2x3':
        columns = ['A', 'B', 'C', 'D', 'E']
        position_map = {
            'A': 'window',
            'B': 'aisle',
            'C': 'middle',
            'D': 'aisle',
            'E': 'window',
        }

    else:
        return HttpResponse(
            "<script>alert('Invalid seat type!');"
            "window.location='/operator/busv/';</script>"
        )

    # Generate seats
    seat_list = []
    for row in range(1, rows + 1):
        for col in columns:
            seat_list.append(
                Seats(
                    bid=bus,
                    seatno=f"{row}{col}",
                    seat_price=742.00,
                    seat_position=position_map[col]
                )
            )

    Seats.objects.bulk_create(seat_list)

    return HttpResponse(
        "<script>alert('Seats generated successfully!');"
        "window.location='/operator/busv/';</script>"
    )

def updatelocation(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    locations = Location.objects.all()
    
    if request.method == "POST":
        loc_id = request.POST('location')
        
        LiveLocation.objects.update_or_create(
            trip=trip,
            defaults={'location_id': loc_id}
        )

        # messages.success(request, "Location updated successfully!")
        return HttpResponse(
        "<script>alert('Location updated successfully!');window.location='';</script>"
    )
    # return redirect('operator:trip_view')

    return render(request, "operator/update_location.html", {
        "trip": trip,
        "locations": locations
    })

# def update_location(request, trip_id):
#     if request.method == "POST":
#         loc_id = request.POST['location']

#         LiveLocation.objects.update_or_create(
#             trip_id=trip_id,
#             defaults={'location_id': loc_id}
#         )

#     return redirect('operator:trip_view')

def add_trip(request):
    busroutes = BusRoutes.objects.all()

    if request.method == "POST":
        busroute_id = request.POST.get('busroute')
        date = request.POST.get('date')

        # Check duplicate trip
        if Trip.objects.filter(busroute_id=busroute_id, date=date).exists():
            return HttpResponse(
                "<script>alert('Trip already exists!');window.location='/operator/add_trip/';</script>"
            )
        
        # Create trip
        Trip.objects.create(
            busroute_id=busroute_id,
            date=date
        )
        
        return HttpResponse(
            "<script>alert('Trip added successfully!');window.location='/operator/trip_view/';</script>"
        )

    return render(request, "add_trip.html", {
        "busroutes": busroutes
    })

def trip_view(request):
    trips = Trip.objects.all().order_by('-date')
    return render(request, "trip_view.html", {"trips": trips})

def view_bookings(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    # We want to see all seats booked for this trip.
    # BookingDetails -> Master -> Trip
    bookings = BookingDetails.objects.filter(master__trip=trip)
    return render(request, "operator/view_bookings.html", {
        "trip": trip,
        "bookings": bookings
    })