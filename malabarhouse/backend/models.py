from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Booking(models.Model):
    guest = models.ForeignKey(User)