from django.contrib import admin
from backend.models import Booking, Room, Extra

# Register your models here.
# TODO: make bookings view prettier
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Extra)