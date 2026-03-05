from django.db import models

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=20)

