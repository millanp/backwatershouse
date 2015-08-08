from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm
# from django.http.response import HttpResponse

# Create your views here.
@login_required
def home(request):
    return render(request, "frontend/home.html", {})
@login_required
def booking(request):
    return render(request, "frontend/booking.html", {'form':BookingForm()})
