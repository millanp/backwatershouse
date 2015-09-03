from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.forms.models import ModelForm
# Create your models here.
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
    rooms = MultiSelectField(choices=ROOMS, default="-")
    extra = MultiSelectField(choices=EXTRAS, default="-", null=True, blank=True)
    approved = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=False)
#IMPORTANT!!!! I need to subclass this in order to let the guest value be preset!!!!!!
class BookingForm(ModelForm):
    class Meta():
        model = Booking
        fields = "__all__"
        exclude = ['guest']