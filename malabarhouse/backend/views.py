from django.shortcuts import render
from django.views.generic.edit import CreateView
from models import Booking, BookingForm
from django.core.urlresolvers import reverse, reverse_lazy
# Create your views here.
class BookingCreate(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = '/booking'