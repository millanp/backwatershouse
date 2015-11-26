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
from django.db.models.signals import post_save, post_init, pre_delete,\
    m2m_changed
from datetime import timedelta, datetime, date
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields.ranges import DateRangeField
from psycopg2._range import DateRange
from django.contrib.postgres.fields.hstore import HStoreField
# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    blurb = models.TextField(max_length=700)
    request_cal_id = models.TextField(null=True, blank=True)
    booking_cal_id = models.TextField(null=True, blank=True)
    rand = models.NullBooleanField()
    def __str__(self):
        return "Room "+str(self.number)

    def request_to_calendar(self, arrive, leave):
        print 'requesting to calendar...'
        event = {
            'summary': 'Request for Room '+str(self.number),
            'start': {
                'date': arrive.isoformat()
            },
            'end': {
                'date': leave.isoformat()
            }
        }
        calapi = cal_api()
        event = calapi.events().insert(calendarId=self.request_cal_id.strip(), body=event).execute()
        return event.get('id')
def delete_calendars(sender, instance, using, **kwargs):
    calapi = cal_api()
    calapi.calendars().delete(calendarId=instance.booking_cal_id.strip()).execute()
    calapi.calendars().delete(calendarId=instance.request_cal_id.strip()).execute()
pre_delete.connect(delete_calendars, sender=Room)
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
        instance.booking_cal_id = calresources[0]['id'] 
        instance.request_cal_id = calresources[1]['id']
        instance.save()
        x = [calapi.acl().insert(calendarId=calresource['id'], body=aclrule).execute() for calresource in calresources]
post_save.connect(create_calendars, sender=Room)
class Booking(models.Model):
    guest = models.ForeignKey(User)
    #add arrive and leave here for input sake, then generate stay
    arrive = models.DateField()
    leave = models.DateField()
    stay = DateRangeField(null=True, blank=True)
    rooms = models.ManyToManyField(Room)
    extra = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    paid_for = models.BooleanField(default=True)
    request_event_ids = HStoreField(null=True, blank=True)
    booking_event_ids = HStoreField(null=True, blank=True)
    def clean(self):
        #check that arrive is before leave
        if self.arrive < self.leave:
            raise ValidationError('Arrival time is after departure time')
        #check that booking is not in the past
        if self.arrive < datetime.now().date():
            raise ValidationError('Booking is in the past')
    def nice_rooms(self):
        return helpers.humanize_list(self.rooms.all())
    nice_rooms.short_description = "Rooms" #hey this is a comment
    def short_description(self):
        return "A visit to " + str(self.nice_rooms()) + " from " + str(self.stay.lower) + " to " + str(self.stay.upper)
    def add_request_to_google(self, pk_set):
        print 'foo'
        for room in Room.objects.filter(pk__in=pk_set):
            print 'asfasdfasdfa'
            self.request_event_ids[str(room.pk)] = room.request_to_calendar(self.arrive, self.leave)
    def payment_button(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "5",
            "item_name": "Malabar House non-family upkeep fee",
            "quantity": "1",
            "currency_code": "USD",
            "env": "www.sandbox",
            "notify_url": settings.SITE_URL+reverse("paypal-responder"),
            "custom": str(self.pk),
        }
        return PayPalPaymentsForm(initial=paypal_dict)
    def approve(self):
        pass 
def fill_stay(sender, instance, created, **kwargs):
    if created:
        instance.stay = DateRange(lower=instance.arrive, upper=instance.leave)
        instance.save()
post_save.connect(fill_stay, sender=Booking)
def post_save_mymodel(sender, instance, action, reverse, pk_set, *args, **kwargs):
    if reverse == False and action == 'post_add':
        instance.add_request_to_google(pk_set)
m2m_changed.connect(post_save_mymodel, sender=Booking.rooms.through)
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = ['arrive', 'leave', 'rooms', 'extra']
    def clean(self):
        overlaps = Booking.objects.filter(
            stay__overlap=DateRange(lower=self.cleaned_data.get('arrive'), 
                                    upper=self.cleaned_data.get('leave'))
            ).filter(rooms__in=self.cleaned_data.get('rooms'))
        if len(overlaps) > 0:
            raise ValidationError('Booking is overlapping another booking')
class BookingAdminForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
    def clean(self):
        overlaps = Booking.objects.filter(
            stay__overlap=DateRange(lower=self.cleaned_data.get('arrive'), 
                                    upper=self.cleaned_data.get('leave'))
            ).filter(rooms__in=self.cleaned_data.get('rooms'))
        if len(overlaps) > 0:
            raise ValidationError('Booking is overlapping another booking')
