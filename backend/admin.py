from django.contrib import admin
from backend.models import Booking, Room, BookingAdminForm
from backend import helpers
# Register your models here.
def set_approved_fee(modeladmin, request, queryset):
    set_approved_base(modeladmin, request, queryset)
    queryset.update(payment_required=True, paid_for=False)
def set_approved_base(modeladmin, request, queryset):
    helpers.notify_guests_booking_approved(queryset)
    queryset.update(approved=True)
def set_approved_free(modeladmin, request, queryset):
    set_approved_base(modeladmin, request, queryset)
    for booking in queryset:
        booking.approve()
set_approved_fee.short_description = "Approve, but charge a fee"
set_approved_free.short_description = "Approve with no fee"

def create_calendars(modeladmin, request, queryset):
    for room in queryset:
        room.create_calendars()
class BookingAdmin(admin.ModelAdmin):
    list_display = ('nice_rooms', 'arrive', 'leave', 'guest',
                    'extra', 'approved', 'payment_required', 'paid_for')
    actions = [set_approved_fee, set_approved_free]
    form = BookingAdminForm
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'request_cal_id', 'booking_cal_id')
    actions = [create_calendars]
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room, RoomAdmin)