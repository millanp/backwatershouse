from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=10)
class Extra(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=10,)
class Booking(models.Model):
    guest = models.ForeignKey(User)
    arrive = models.DateField()
    leave = models.DateField()
    rooms = models.ManyToManyField(Room)
    extra = models.ManyToManyField(Extra)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)