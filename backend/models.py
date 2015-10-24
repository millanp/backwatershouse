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
# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    blurb = models.TextField(max_length=700)
    def __str__(self):
        return "Room "+str(self.number)
    def get_booking_calendar_id(self):
        pass
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
