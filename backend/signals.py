from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_recieved
from django.dispatch.dispatcher import receiver
from paypal.standard.models import ST_PP_COMPLETED
from backend.models import Booking
import logging
@receiver(valid_ipn_received)
def callback(ipn_obj, **kwargs):
	
    bookings = Booking.objects.all()
    bookings.update(paid_for=True)
#    logger = logging.getLogger('testlogger')
#    logger.info('LOLOLOLOLOLOLOL LOLOLOLO LOLOLOLOLO LOLO LO LOLOLOLOLLOL')
#    if ipn_obj.payment_status == ST_PP_COMPLETED:
#        booking = Booking.objects.filter(pk=eval(ipn_obj.custom))
#        booking.update(paid_for=True)
@receiver(invalid_ipn_recieved)
def cal(ipn_object, **kwargs):
    logger = logging.getLogger('testlogger')
    logger.info('LOLOLOLOLOLOLOL LOLOLOLO LOLOLOLOLO LOLO LO LOLOLOLOLLOL')
