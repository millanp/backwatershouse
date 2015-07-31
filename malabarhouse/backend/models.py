from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Booking(models.Model):
    ROOM_CHOICES = (
        ('1','Room 1'),
        ('2','Room 2'),
        ('3','Room 3'),
        ('4','Room 4')
    )
    EXTRAS = (
        ('1','Extra 1'),
        ('2','Extra 2'),
        ('3','Extra 3'),
    )
    guest = models.ForeignKey(User)
    arrive = models.DateField()
    leave = models.DateField()
    rooms = models.CharField(max_length=1, choices=ROOM_CHOICES)
    extras = models.CharField(max_length=1, choices=EXTRAS)
    approved = models.BooleanField()
    def approve(modeladmin, request, queryset):
        queryset.update(approved=True)
        approve.short_description = "Approve this request"
    #     extras ...