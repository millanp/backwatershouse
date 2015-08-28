from django.shortcuts import render
from django.views.generic.edit import CreateView
from models import Booking, BookingForm
# Create your views here.
class BookingCreate(CreateView):
    model = Booking
    form_class = BookingForm