from django.contrib import admin
from backend.models import Booking

# Register your models here.
# TODO: make bookings view prettier
def set_approved_fee(modeladmin, request, queryset):
    queryset.update(approved=True)
    queryset.update(payment_required=True)
def set_approved_free(modeladmin, request, queryset):
    queryset.update(approved=True)
set_approved_fee.short_description = "Approve, but charge a fee"
set_approved_free.short_description = "Approve with no fee"

def roomList(obj):
    return obj.get_rooms_display()
def extraList(obj):
    return obj.get_extra_display()
roomList.short_description = "Rooms"
extraList.short_description = "Extras"

class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'arrive', 'leave', roomList, 
                    extraList, 'approved', 'payment_required')
    actions = [set_approved_fee, set_approved_free]

admin.site.register(Booking, BookingAdmin)