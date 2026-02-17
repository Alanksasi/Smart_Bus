from django.db import models

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=20)
    
class Location(models.Model):
    loc = models.CharField(max_length=15)
    dis = models.ForeignKey(District,on_delete=models.CASCADE,blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    img = models.ImageField(upload_to="media/",null=True,blank=True)