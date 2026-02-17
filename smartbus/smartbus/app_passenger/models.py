from django.db import models 
from app_dashboard.models import Passenger
from app_operator.models import Seats, Trip

# Create your models here.

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    
class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10,
        default="pending"
    )