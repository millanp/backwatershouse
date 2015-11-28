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
    def book_to_calendar(self, arrive, leave):
        print 'booking to calendar...'
        event = {
            'summary': 'Booking for Room '+str(self.number),
            'start': {
                'date': arrive.isoformat()
            },
            'end': {
                'date': leave.isoformat()
            }
        }
        calapi = cal_api()
        event = calapi.events().insert(calendarId=self.booking_cal_id.strip(), body=event).execute()
        return event.get('id')
    def delete_event(self, eventId, request=False):
        calapi = cal_api()
        if request:
            calendarid = self.request_cal_id.strip()
        else:
            calendarid = self.booking_cal_id.strip()
        calapi.events().delete(calendarId=calendarid, eventId=eventId).execute()
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
    request_event_ids = HStoreField(blank=True, default={})
    booking_event_ids = HStoreField(blank=True, default={})
    def nice_rooms(self):
        return helpers.humanize_list(self.rooms.all())
    nice_rooms.short_description = "Rooms" #hey this is a comment
    def short_description(self):
        return "A visit to " + str(self.nice_rooms()) + " from " + str(self.stay.lower) + " to " + str(self.stay.upper)
    def add_request_to_google(self, pk_set):
        print 'adding request to google'
        for room in Room.objects.filter(pk__in=pk_set):
            print 'rooming'
            self.request_event_ids[str(room.pk)] = room.request_to_calendar(self.arrive, self.leave)
            self.save()
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
    #tested
    def reject(self):
        for roomPkString in self.request_event_ids:
            room = Room.objects.get(pk=eval(roomPkString))
            room.delete_event(self.request_event_ids[roomPkString], request=True)
    def approve(self):
        for roomPkString in self.request_event_ids:
            room = Room.objects.get(pk=eval(roomPkString))
            room.delete_event(self.request_event_ids[roomPkString], request=True)
            room.book_to_calendar(self.arrive, self.leave)
def fill_stay(sender, instance, created, **kwargs):
    if created:
        instance.stay = DateRange(lower=instance.arrive, upper=instance.leave)
        instance.save()
post_save.connect(fill_stay, sender=Booking)
def post_save_mymodel(sender, instance, action, reverse, pk_set, *args, **kwargs):
    if reverse == False and action == 'post_add':
        instance.add_request_to_google(pk_set)
m2m_changed.connect(post_save_mymodel, sender=Booking.rooms.through)

def booking_form_clean(self):
    if self.cleaned_data.get('arrive') and self.cleaned_data.get('leave') and self.cleaned_data.get('rooms'):
        if self.cleaned_data.get('arrive') < datetime.now().date():
            raise ValidationError('Booking is in the past')
        if self.cleaned_data.get('arrive') > self.cleaned_data.get('leave'):
            raise ValidationError('Arrival time is after departure time')
        overlaps = Booking.objects.filter(
            stay__overlap=DateRange(lower=self.cleaned_data.get('arrive'), 
                                    upper=self.cleaned_data.get('leave'))
            ).filter(rooms__in=self.cleaned_data.get('rooms')
            ).filter(approved=True)
        if len(overlaps) > 0:
            raise ValidationError('Booking is overlapping another booking')
    
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = ['arrive', 'leave', 'rooms', 'extra']
    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        booking_form_clean(self)
        
class BookingAdminForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
    def clean(self):
        cleaned_data = super(BookingAdminForm, self).clean()
        booking_form_clean(self)
