from django.db import models
from django.contrib.auth.models import User
from floppyforms.__future__ import ModelForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from backend import helpers
from django.core.urlresolvers import reverse
from backend.helpers import cal_api
from django.db.models.signals import post_save, \
    m2m_changed
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields.ranges import DateRangeField
from psycopg2._range import DateRange
from django.contrib.postgres.fields.hstore import HStoreField
from django.core.mail import mail_admins
from django.contrib.sites.models import Site
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
            'summary': 'Room '+str(self.number)+' booking',
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
    def create_calendars(self):
        calapi = cal_api()
        newcals = [
            {'summary':str(self),},
            {'summary':'Requests for '+str(self)}
        ]
        calresources = [calapi.calendars().insert(body=newcal).execute() for newcal in newcals]
        aclrule = {
            'role':'owner',
            'scope':{
                'type':'user',
                'value':'millan.philipose@gmail.com'
            }
        }
        publicacl = {
            'role':'reader',
            'scope':{
                'type':'default'
            }
        }
        self.booking_cal_id = calresources[0]['id'] 
        self.request_cal_id = calresources[1]['id']
        self.save()
        for res in calresources:
            calapi.acl().insert(calendarId=res['id'], body=aclrule).execute()
            calapi.acl().insert(calendarId=res['id'], body=publicacl).execute()
    def request_to_calendar(self, arrive, leave):
        print 'requesting to calendar...'
        event = {
            'summary': 'Room '+str(self.number)+' request',
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
def create_calendars(sender, instance, created, **kwargs):
    # created means just created
    if created:
        instance.create_calendars()
post_save.connect(create_calendars, sender=Room)


class Booking(models.Model):
    guest = models.ForeignKey(User)
    # add arrive and leave here for input sake, then generate state
    arrive = models.DateField(verbose_name='Arrival')
    leave = models.DateField(verbose_name='Departure')
    stay = DateRangeField(null=True, blank=True)
    rooms = models.ManyToManyField(Room)
    extra = models.BooleanField(default=False, verbose_name='Housekeeping services desired')
    # different states of approval that the stay request could be in
    AWAITING_OWNER_APPROVAL = 1
    PAYMENT_NEEDED = 2
    FINALIZED_PAID = 3
    FINALIZED_FREE = 4
    REJECTED = 5
    APPROVAL_STATE_CHOICES = (
        (AWAITING_OWNER_APPROVAL, 'Awaiting owner approval'),
        (PAYMENT_NEEDED, 'Approved; waiting for payment'),
        (FINALIZED_PAID, 'Paid for, finalized, and scheduled'),
        (FINALIZED_FREE, 'Finalized and scheduled'),
        (REJECTED, 'Rejected'),
    )
    approval_state = models.PositiveSmallIntegerField(choices=APPROVAL_STATE_CHOICES, default=AWAITING_OWNER_APPROVAL)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    paid_for = models.BooleanField(default=True)
    request_event_ids = HStoreField(blank=True, default={}, null=True)
    booking_event_ids = HStoreField(blank=True, default={}, null=True)

    def nice_rooms(self):
        return helpers.humanize_list(self.rooms.all())
    nice_rooms.short_description = "Rooms"  # hey this is a comment

    def finalized(self):
        return self.approval_state >= self.FINALIZED_PAID
    finalized.boolean = True

    def status_color(self):
        if self.approval_state == self.PAYMENT_NEEDED:
            return "orange"
        elif self.approval_state == self.AWAITING_OWNER_APPROVAL:
            return ""  # to make the html render default color
        elif self.approval_state >= self.FINALIZED_PAID:
            return "green"

    def short_description(self):
        return "A visit to " + str(self.nice_rooms()) + " from " + str(self.stay.lower) + " to " + str(self.stay.upper)

    def add_request_to_google(self, pk_set):
        print 'adding request to google'
        for room in Room.objects.filter(pk__in=pk_set):
            print 'rooming'
            self.request_event_ids[str(room.pk)] = room.request_to_calendar(self.arrive, self.leave)
            self.save()

    def payment_fields(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "5",
            "item_name": "%s non-family upkeep fee" % (settings.VENUE_NAME),
            "quantity": "1",
            "currency_code": "USD",
            "env": "www.sandbox",
            "notify_url": settings.SITE_URL+reverse("paypal-ipn"),
            "custom": str(self.pk),
        }
        return PayPalPaymentsForm(initial=paypal_dict)

    # tested
    def reject(self):
        for roomPkString in self.request_event_ids:
            room = Room.objects.get(pk=eval(roomPkString))
            room.delete_event(self.request_event_ids[roomPkString], request=True)
        self.delete()

    def require_payment(self):
        self.approval_state = self.PAYMENT_NEEDED
        self.save()
        overlaps = Booking.objects.filter(
            stay__overlap=DateRange(lower=self.arrive, 
                                    upper=self.leave)
            ).filter(rooms__in=self.rooms.all()
            ).filter(approval_state__lt=self.FINALIZED_PAID
            ).exclude(pk=self.pk)
        for booking in overlaps:
            booking.reject()

    def approve(self, payment_required=False):
        if payment_required:
            self.approval_state = self.FINALIZED_PAID
        else:
            self.approval_state = self.FINALIZED_FREE
            for roomPkString in self.request_event_ids:
                room = Room.objects.get(pk=eval(roomPkString))
                room.delete_event(self.request_event_ids[roomPkString], request=True)
                room.book_to_calendar(self.arrive, self.leave)
                overlaps = Booking.objects.filter(
                    stay__overlap=DateRange(lower=self.arrive, 
                                            upper=self.leave)
                    ).filter(rooms__in=self.rooms.all()
                    ).filter(approval_state__lt=self.FINALIZED_PAID
                    ).exclude(pk=self.pk)
                for booking in overlaps:
                    booking.reject()
        self.save()

    def get_fee(self):
        return getattr(settings, "BOOKING_FEE", "$5")

def fill_stay(sender, instance, created, **kwargs):
    if created:
        instance.stay = DateRange(lower=instance.arrive, upper=instance.leave)
        instance.save()
        mail_admins('Someone requested a stay at %s' % (settings.VENUE_NAME),
                    'Click here to take action '+Site.objects.get_current().domain+reverse('admin:backend_booking_changelist')
                    )
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
            ).filter(approval_state__gte=Booking.FINALIZED_PAID)
        if len(overlaps) > 0:
            raise ValidationError('Booking is overlapping another booking')


class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = ['arrive', 'leave', 'rooms', 'extra']

    def clean(self):
        if self.cleaned_data.get('arrive') and self.cleaned_data.get('leave') and self.cleaned_data.get('rooms'):
            if self.cleaned_data.get('arrive') < datetime.now().date():
                raise ValidationError('Booking is in the past')
            if self.cleaned_data.get('arrive') > self.cleaned_data.get('leave'):
                raise ValidationError('Arrival time is after departure time')
            if self.cleaned_data.get('arrive') == self.cleaned_data.get('leave'):
                raise ValidationError('Arrival time is the same as departure time')
            overlaps = Booking.objects.filter(
                stay__overlap=DateRange(lower=self.cleaned_data.get('arrive'), 
                                        upper=self.cleaned_data.get('leave'))
                ).filter(rooms__in=self.cleaned_data.get('rooms')
                ).filter(approval_state__gte=Booking.FINALIZED_PAID)
            if len(overlaps) > 0:
                raise ValidationError('Rooms not available on selected dates')
# class RoomsSelect(widgets.SelectMultiple):
#     def render_option(self, selected_choices, option_value, option_label):
#         widget = widgets.SelectMultiple.render_option(self, selected_choices, option_value, option_label)
#         split_widget = widget.split(">")
#         image_url = 
class BookingAdminForm(ModelForm):
    class Meta():
        model = Booking
        fields = ['guest', 'arrive', 'leave', 'rooms', 'extra']
    def clean(self):
        cleaned_data = super(BookingAdminForm, self).clean()
        booking_form_clean(self)

class RoomAdminForm(ModelForm):
    class Meta():
        model = Room
        fields = ['number', 'blurb']