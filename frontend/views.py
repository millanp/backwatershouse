from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm, Booking, Room
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
from malabarhouse import settings
from django.http.response import JsonResponse, HttpResponse
from backend import colors
def google_calendar_url():
    prefix = r"https://www.google.com/calendar/embed?title=Malabar%20House%20Bookings&height=600&wkst=1&bgcolor=%23FFFFFF&"
    suffix = r"ctz=America%2FLos_Angeles"
    color = 0
    for room in Room.objects.all():
        thiscal = "src="+room.request_cal_id.strip()+"&color=%23"+colors.COLORS[color]+"&"
        prefix += thiscal
        color += 1
    prefix += suffix
    return prefix
class BookingCreate(LoginRequiredMixin, CreateView, ):
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.guest = self.request.user
        obj.save()
        super(CreateView, self).form_valid(form)
        return HttpResponse(form.as_p())
    def form_invalid(self, form):
        return HttpResponse(form.as_p(), status=400)
    def google_calendar_url(self):
        prefix = r"https://www.google.com/calendar/embed?title=Malabar%20House%20Bookings&height=600&wkst=1&bgcolor=%23FFFFFF&"
        suffix = r"ctz=America%2FLos_Angeles"
        color = 0
        for room in Room.objects.all():
            thiscal = "src="+room.request_cal_id.strip()+"&color=%23"+colors.CLUT[color][1]+"&"
            prefix += thiscal
        prefix += suffix
        return prefix
    def get_context_data(self, **kwargs):
        return {'cal_url':google_calendar_url()}
        
#         return JsonResponse(form.errors, status=400)
# Create your views here.
class TemplateViewPlus(LoginRequiredMixin, TemplateView):
    template_name = "frontend/home.html"
    context = {}
    def get_context_data(self, **kwargs):
        return self.context;
@login_required
def requestsView(request):
    print 'displaying requests'
    return render(request, 
        'frontend/requests.html', 
        {'bookings':Booking.objects.filter(guest=request.user)},
    )
