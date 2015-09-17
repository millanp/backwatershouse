from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.forms.models import ModelForm
from paypal.standard.forms import PayPalPaymentsForm
from malabarhouse import settings
import helpers
# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    def __str__(self):
        return "Room "+str(self.number)
class Booking(models.Model):
    ROOMS = (
        ('1', 'Room 1'),
        ('2', 'Room 2'),
        ('3', 'Room 3'),
    )
    EXTRAS = (
        ('1', 'Extra1'),
        ('2', 'Extra2'),
        ('3', 'Extra3')
    )
    guest = models.ForeignKey(User)
    arrive = models.DateField()
    leave = models.DateField()
    rooms = models.ManyToManyField(Room)
    extra = models.BooleanField()
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
    def get_rooms_nicelist(self):
        return helpers.humanize_list(self.rooms.all())
    def short_description(self):
        return "A visit to " + str(self.get_rooms_display()) + " from " + str(self.arrive) + " to " + str(self.leave)
    
    def payment_button(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "5",
            "item_name": "Malabar House non-family upkeep fee",
            "quantity": "1",
            "currency_code": "USD",
            "env": "www.sandbox",
            "notify_url": "", #TODO
            "custom": str(self.pk),
        }
        return PayPalPaymentsForm(initial=paypal_dict)
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
        exclude = ['guest']