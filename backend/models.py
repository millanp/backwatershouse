from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from paypal.standard.forms import PayPalPaymentsForm
from malabarhouse import settings
from backend import helpers
from django.core.urlresolvers import reverse
from malabarhouse import settings
import os
from oauth2client.client import SignedJwtAssertionCredentials
from googleapiclient.discovery import build
from httplib2 import Http
from backend.helpers import cal_api
from django.db.models.signals import post_save, post_init
# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    blurb = models.TextField(max_length=700)
    request_cal_id = models.TextField()
    booking_cal_id = models.TextField()
    rand = models.NullBooleanField()
    def __str__(self):
        return "Room "+str(self.number)
    def get_booking_calendar_id(self):
        calendarapi = cal_api()
        cal_list = calendarapi.calendarList().list(minAccessRole="writer").execute()
        for cal in cal_list:
            print cal['summary']

def create_calendars(sender, instance, created, **kwargs):
    if created:
        calapi = cal_api()
        newcals = [
            {'summary':str(instance),},
            {'summary':'Requests for '+str(instance)}
        ]
        calresources = [calapi.calendars().insert(body=newcal).execute() for newcal in newcals]
        aclrule = {
            'role':'owner',
            'scope':{
                'type':'user',
                'value':'millan.philipose@gmail.com'
            }
        }
        instance.update(booking_cal_id=calresources[0]['id'], request_cal_id=calresources[1]['id'])
        x = [calapi.acl().insert(calendarId=calresource['id'], body=aclrule).execute() for calresource in calresources]
post_save.connect(create_calendars, sender=Room)
class Booking(models.Model):
    guest = models.ForeignKey(User)
    arrive = models.DateField()
    leave = models.DateField()
    rooms = models.ManyToManyField(Room)
    extra = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    paid_for = models.BooleanField(default=True)
    def __init__(self, *args, **kwargs):
        self.add_request_to_google()
        models.Model.__init__(self, *args, **kwargs)
    def nice_rooms(self):
        return helpers.humanize_list(self.rooms.all())
    nice_rooms.short_description = "Rooms"
    def short_description(self):
        return "A visit to " + str(self.nice_rooms()) + " from " + str(self.arrive) + " to " + str(self.leave)
    def add_request_to_google(self):
        credential = SignedJwtAssertionCredentials(
            os.environ['GOOGLE_CLIENT_EMAIL'],
            os.environ['GOOGLE_PRIVATE_KEY'].encode(),
            'https://www.googleapis.com/auth/calendar',
        )
        http_auth = credential.authorize(Http())
        calendarapi = build('calendar', 'v3', http=http_auth)
    def payment_button(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "5",
            "item_name": "Malabar House non-family upkeep fee",
            "quantity": "1",
            "currency_code": "USD",
            "env": "www.sandbox",
            "notify_url": settings.SITE_URL+reverse("paypal-responder"), #TODO
            "custom": str(self.pk),
        }
        return PayPalPaymentsForm(initial=paypal_dict)
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
        exclude = ['guest']
