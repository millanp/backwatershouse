from django.core import mail
from malabarhouse import settings
def notify_guests_booking_approved(bookings):
    for booking in bookings:
        booking.guest.email_user(
            "Your booking request has been approved",
            "Please visit your My Requests page to finalize",
        )
def humanize_list(xlist):
    if len(xlist) == 1:
        return xlist[0]
    elif len(xlist) == 0:
        return ""
    xlist = map(str, xlist)
    return ", ".join(xlist[:len(xlist)-1]) + " and " + xlist[len(xlist)-1]