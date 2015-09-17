from django.core import mail
from malabarhouse import settings
def notify_guests_booking_approved(bookings):
    for booking in bookings:
        booking.guest.email_user(
            "Your booking request has been approved",
            "Please visit your My Requests page to finalize",
        )
def humanize_list(value):
#     if len(value) == 0:
#         return ""
#     elif len(value) == 1:
#         return value[0]
#     s = ", ".join(value[:len(value)-2])
#     if len(value) > 3:
#         s += ","
#     return "%s and %s" % (s, value[len(value)-2])
    return str(value)