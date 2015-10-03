from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch.dispatcher import receiver
from paypal.standard.models import ST_PP_COMPLETED
from backend.models import Booking
@receiver(valid_ipn_received)
def callback(ipn_obj, **kwargs):
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        booking = Booking.objects.filter(pk=eval(ipn_obj.custom))
        booking.update(paid_for=True)