from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Booking, BookingForm
from django.core.urlresolvers import reverse, reverse_lazy
import requests
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class BookingCreate(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
@csrf_exempt
def paypal_processer(request):
    reqDict = request.POST.dict()
    b = Booking.objects.filter(pk=eval(reqDict['custom']))
    b.update(paid_for=True)
    r = requests.post("https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&", params=reqDict)
    
    