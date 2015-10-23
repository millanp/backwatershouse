from django.core import mail
from malabarhouse import settings
from oauth2client.client import SignedJwtAssertionCredentials
import os
from httplib2 import Http
from googleapiclient.discovery import build
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
def calendar_test():
#     credential = SignedJwtAssertionCredentials 2015-12-23T07:00:00+07:00
    credential = SignedJwtAssertionCredentials(
        os.environ['GOOGLE_CLIENT_EMAIL'],
        os.environ['GOOGLE_PRIVATE_KEY'],
        'https://www.googleapis.com/auth/calendar',
    )
    print os.environ['GOOGLE_PRIVATE_KEY']
    http_auth = credential.authorize(Http())
    calendarapi = build('calendar', 'v3', http=http_auth)
    event = {
        'summary': '(roomOnCalendarEvent)',
        'location': 'Malabar House',
        'start': {
            'date':'startDate.toISOString().slice(0,10)',
        },
        'end': {
            'date':'2015-12-23T07:00:00+07:00',
        },
   
    }
    calendarapi.events().insert('icoufgc83qm32aer4nuc3k9fjo@group.calendar.google.com', event)