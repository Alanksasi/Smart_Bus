from django.db import models
from app_core.models import District
from smartbus.users.models import User

# Create your models here.
class Operator(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,default=2)
    dis = models.ForeignKey(District,on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=10,unique=True)

class Passenger(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,default=2)
    contact = models.CharField(max_length=10,unique=True)