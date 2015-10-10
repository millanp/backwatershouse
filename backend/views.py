from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Booking, BookingForm
from django.core.urlresolvers import reverse, reverse_lazy
import requests
from django.core.mail import send_mail
# Create your views here.
class BookingCreate(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
def paypal_processer(request):
    send_mail('ff', 'ff', 'donotreply@mala.com', ['millan.philipose@gmail.com'])
    b = Booking.objects.all()
    b.update(paid_for=True)
    r = requests.post("https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&", params=request.POST.dict())
    
    