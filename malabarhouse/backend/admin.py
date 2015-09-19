from django.contrib import admin
from backend.models import Booking, Room
from backend import helpers
# Register your models here.
def set_approved_fee(modeladmin, request, queryset):
    set_approved_free(modeladmin, request, queryset)
    queryset.update(payment_required=True, paid_for=True)
    
def set_approved_free(modeladmin, request, queryset):
    helpers.notify_guests_booking_approved(queryset)
    queryset.update(approved=True)
    
set_approved_fee.short_description = "Approve, but charge a fee"
set_approved_free.short_description = "Approve with no fee"

def roomList(obj):
    return obj.get_rooms_nicelist()
roomList.short_description = "Rooms"
class BookingAdmin(admin.ModelAdmin):
    list_display = (roomList, 'arrive', 'leave', 'guest',
                    'extra', 'approved', 'payment_required', 'paid_for')
    actions = [set_approved_fee, set_approved_free]
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room, RoomAdmin)