from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm, Booking
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
# from django.http.response import HttpResponse
class BookingCreate(CreateView):
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
# Create your views here.
class TemplateViewPlus(TemplateView, LoginRequiredMixin):
    template_name = "frontend/home.html"
    context = {}
    def get_context_data(self, **kwargs):
        return self.context;
@login_required
def home(request):
    return render(request, "frontend/home.html", {})
@login_required
def booking(request):
    return render(request, "frontend/booking.html", {'form':BookingForm()})
