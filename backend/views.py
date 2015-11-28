from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Booking, BookingForm
from django.core.urlresolvers import reverse, reverse_lazy
import requests
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from malabarhouse import settings
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
class BookingCreate(SuccessMessageMixin, CreateView):
    model = Booking
    form_class = BookingForm
    success_url = '/booking'
    success_message = 'Booking submitted successfully'
    template_name = 'frontend/booking.html'
@csrf_exempt
def paypal_processer(request):
    reqDict = request.POST.dict()
    r = requests.post("https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&", params=reqDict)
    if r.text == "VERIFIED":
        if settings.PAYPAL_TEST:
            b = Booking.objects.get(pk=eval(reqDict['custom']))
            b.paid_for=True
            b.save()
            b.approve()
        else:
            if reqDict['payment_status'] == "Confirmed":
                b = Booking.objects.get(pk=eval(reqDict['custom']))
                b.paid_for=True
                b.save()
                b.approve()