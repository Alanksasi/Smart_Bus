from django.db import models
from smartbus.users.models import User

# Create your models here.
class BusReg(models.Model):
    name = models.CharField(max_length=20)
    num = models.CharField(max_length=15, unique=True)
    con = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    seat_type = models.CharField(
        max_length=5,
        choices=(('2x2', '2 x 2'), ('2x3', '2 x 3'))
    )
    total_rows = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.num})"
    
class Routes(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50) 
       
class BusRoutes(models.Model):
    bid = models.ForeignKey(BusReg,on_delete=models.CASCADE,blank=True)
    rid = models.ForeignKey(Routes,on_delete=models.CASCADE,blank=True)
    time = models.TimeField()

    def __str__(self):
        return f"{self.bid.name} - {self.rid.name} ({self.time})"
    
class RouteStop(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.IntegerField()
    
    class Meta:
        ordering = ['order']

# class Seats(models.Model):
#     bid = models.ForeignKey(BusReg, on_delete=models.CASCADE, blank=True)
#     seatno = models.CharField(max_length=15)
#     is_booked = models.BooleanField(default=False)

class Seats(models.Model):
    POSITION_CHOICES = (
        ('window', 'Window'),
        ('aisle', 'Aisle'),
        ('middle', 'Middle'),   # used only in 2x3
    )
    bid = models.ForeignKey(BusReg, on_delete=models.CASCADE)
    seatno = models.CharField(max_length=15)
    seat_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=742.00
    )
    seat_position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,null=True,blank=True
    )
    is_booked = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.seatno} - {self.seat_position}"

# class Trip(models.Model):
#     busroute = models.ForeignKey(BusRoutes, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(
#         max_length=10,
#         choices=(('scheduled', 'Scheduled'), ('running', 'Running'), ('completed', 'Completed')),
#         default='scheduled'
#     )

# class Trip(models.Model):
#     busroute = models.ForeignKey(BusRoutes, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(
#         max_length=10,
#         choices=(('scheduled', 'Scheduled'), ('running', 'Running'), ('completed', 'Completed')),
#         default='scheduled'
#     )

class Trip(models.Model):
    busroute = models.ForeignKey(BusRoutes, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=(
            ('scheduled', 'Scheduled'),
            ('running', 'Running'),
            ('completed', 'Completed')
        ),
        default='scheduled'
    )

    def __str__(self):
        return f"{self.busroute.bid.name} - {self.date}"

class LiveLocation(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
