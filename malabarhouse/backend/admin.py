from django.contrib import admin
from backend.models import Booking, Room, Extra

# Register your models here.
# TODO: make bookings view prettier
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'arrive', 'leave', 'rooms')
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room)
admin.site.register(Extra)