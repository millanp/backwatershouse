from paypal.standard.ipn.signals import invalid_ipn_received, valid_ipn_received
from django.dispatch.dispatcher import receiver
from paypal.standard.models import ST_PP_COMPLETED
from backend.models import Booking
import logging


@receiver(valid_ipn_received)
def callback(ipn_obj, **kwargs):
    bookings = Booking.objects.all()
    bookings.update(approval_state=Booking.FINALIZED_PAID)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        booking = Booking.objects.filter(pk=eval(ipn_obj.custom))
        booking.update(paid_for=True)


@receiver(invalid_ipn_received)
def cal(ipn_object, **kwargs):
    bookings = Booking.objects.all()
    bookings.update(approval_state=Booking.FINALIZED_PAID)
