from django.contrib import admin
from backend.models import Booking, Room, BookingAdminForm, RoomAdminForm
from backend import helpers
from django.contrib.auth.models import Group
from paypal.standard.ipn.models import PayPalIPN
from django.contrib.sites.models import Site
# Register your models here.
def set_approved_fee(modeladmin, request, queryset):
    set_approved_base(modeladmin, request, queryset, payment_required=True)
    
def set_approved_base(modeladmin, request, queryset, payment_required=False):
    helpers.notify_guests_booking_approved(queryset)
    for booking in queryset:
        if not payment_required:
            booking.approve()
        else:
            booking.require_payment()
def set_approved_free(modeladmin, request, queryset):
    set_approved_base(modeladmin, request, queryset)
def set_rejected(modeladmin, request, queryset):
    helpers.notify_guests_booking_rejected(queryset)
    for booking in queryset:
        booking.reject()
set_approved_fee.short_description = "Approve, but charge a fee"
set_approved_free.short_description = "Approve with no fee"
set_rejected.short_description = "Reject requests"
def create_calendars(modeladmin, request, queryset):
    for room in queryset:
        room.create_calendars()
class BookingAdmin(admin.ModelAdmin):
    list_display = ('nice_rooms', 'arrive', 'leave', 'guest',
                    'extra', 'approval_state')
    actions = [set_approved_fee, set_approved_free, set_rejected]
    ordering = ['approval_state']
    form = BookingAdminForm
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'request_cal_id', 'booking_cal_id')
    actions = [create_calendars]
    form = RoomAdminForm
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room, RoomAdmin)

admin.site.unregister(Group)
admin.site.unregister(PayPalIPN)
admin.site.unregister(Site)