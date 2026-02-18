from django.db import models 
from app_dashboard.models import Passenger
from app_operator.models import Seats, Trip

# Create your models here.

class BookingMaster(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10,
        default="pending"
    )

    def __str__(self):
        return f"Booking {self.id} - {self.passenger.name}"

class BookingDetails(models.Model):
    master = models.ForeignKey(BookingMaster, on_delete=models.CASCADE, related_name='details')
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.master.id} - {self.seat.seatno}"
