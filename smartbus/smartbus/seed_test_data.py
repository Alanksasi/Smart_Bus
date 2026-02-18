import os
import django
from datetime import date, time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartbus.settings')
django.setup()

from django.contrib.auth import get_user_model
from app_dashboard.models import Passenger
from app_operator.models import BusReg, Routes, BusRoutes, Trip, Seats

User = get_user_model()

def seed():
    print("Seeding data...")
    # 1. Create User & Passenger
    user, created = User.objects.get_or_create(username='test_passenger', email='test@example.com')
    if created:
        user.set_password('password123')
        user.save()
        print("Created user 'test_passenger'")
    else:
        print("User 'test_passenger' already exists")
    
    passenger, created = Passenger.objects.get_or_create(user=user, defaults={
        'name': "Test Passenger",
        'ph': "1234567890",
        'address': "Test Address",
        'id_proof': "Proof"
    })
    if created:
        print("Created Passenger profile")

    # Operator User (for BusReg)
    op_user, created = User.objects.get_or_create(username='test_operator', email='op@example.com')
    if created:
        op_user.set_password('password123')
        op_user.save()
        print("Created user 'test_operator'")

    # 2. Create Route
    route, created = Routes.objects.get_or_create(name="Test Route - City A to City B")
    print(f"Route: {route.name}")

    # 3. Create Bus (2x2)
    bus, created = BusReg.objects.get_or_create(num="TB-1234", defaults={
        'name': 'Test Bus Luxury',
        'con': '9876543210',
        'user': op_user,
        'seat_type': '2x2',
        'total_rows': 5
    })
    print(f"Bus: {bus.name} ({bus.seat_type})")

    # 4. Create BusRoute
    bus_route, created = BusRoutes.objects.get_or_create(bid=bus, rid=route, defaults={'time': time(10, 0)})
    print("BusRoute linked")

    # 5. Create Trip for Today
    today = date.today()
    trip, created = Trip.objects.get_or_create(busroute=bus_route, date=today, defaults={'status': 'scheduled'})
    print(f"Trip for {today}: {trip.status}")

    # 6. Create Seats
    # 2x2 = 4 seats per row. 5 rows = 20 seats.
    if not Seats.objects.filter(bid=bus).exists():
        print("Creating seats...")
        for i in range(1, 21):
            seat_num = f"S{i}"
            # Logic for position: 1=Window, 2=Aisle, 3=Aisle, 4=Window (simplified)
            pos_idx = (i - 1) % 4
            if pos_idx == 0 or pos_idx == 3:
                pos = 'window'
            else:
                pos = 'aisle'
                
            Seats.objects.create(
                bid=bus, 
                seatno=seat_num,
                seat_price=500.00,
                seat_position=pos
            )
        print("Seats created.")
    else:
        print("Seats already exist")

if __name__ == '__main__':
    seed()
