from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from paypal.standard.forms import PayPalPaymentsForm
from malabarhouse import settings
from backend import helpers
from django.core.urlresolvers import reverse
# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    blurb = models.TextField(max_length=700)
    def __str__(self):
        return "Room "+str(self.number)
class Booking(models.Model):
    guest = models.ForeignKey(User)
    arrive = models.DateField()
    leave = models.DateField()
    rooms = models.ManyToManyField(Room)
    extra = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    paid_for = models.BooleanField(default=True)
    def nice_rooms(self):
        return helpers.humanize_list(self.rooms.all())
    nice_rooms.short_description = "Rooms"
    def short_description(self):
        return "A visit to " + str(self.nice_rooms()) + " from " + str(self.arrive) + " to " + str(self.leave)
    def payment_button(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "5",
            "item_name": "Malabar House non-family upkeep fee",
            "quantity": "1",
            "currency_code": "USD",
            "env": "www.sandbox",
            "notify_url": settings.SITE_URL+reverse("paypal-ipn"), #TODO
            "custom": str(self.pk),
        }
        return PayPalPaymentsForm(initial=paypal_dict)
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
        exclude = ['guest']
