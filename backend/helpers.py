from django.core import mail
from malabarhouse import settings
from oauth2client.client import SignedJwtAssertionCredentials, GoogleCredentials
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
def cal_api():
    credential = SignedJwtAssertionCredentials(
        os.environ['GOOGLE_CLIENT_EMAIL'],
        os.environ['GOOGLE_PRIVATE_KEY'].encode(),
        'https://www.googleapis.com/auth/calendar',
    )
    http_auth = credential.authorize(Http())
    calendarapi = build('calendar', 'v3', http=http_auth)
    return calendarapi
def calendar_testget():
    credential = SignedJwtAssertionCredentials(
        os.environ['GOOGLE_CLIENT_EMAIL'],
        os.environ['GOOGLE_PRIVATE_KEY'].encode(),
        'https://www.googleapis.com/auth/calendar',
    )
    http_auth = credential.authorize(Http())
    calapi = build('calendar', 'v3', http=http_auth)
    cal_list = calapi.calendarList().list(minAccessRole="reader").execute()
    print cal_list
    for cal in cal_list['items']:
        print cal['summary']
def calendar_test_create_share():
    calapi = cal_api()
    newcal = {
        'summary':'DEEZ CAL',
    }
    calapi.calendars().insert(body=newcal).execute()
def calendar_testev():
#     credential = SignedJwtAssertionCredentials 2015-12-23T07:00:00+07:00

    calendarapi = cal_api()
    event = {
        'summary': '(roomOnCalendarEvent)',
        'location': 'Malabar House',
        'start': {
            'date':'2015-12-23',
        },
        'end': {
            'date':'2015-12-24',
        },
   
    }
    calendarapi.events().insert(calendarId='icoufgc83qm32aer4nuc3k9fjo@group.calendar.google.com', body=event).execute()
