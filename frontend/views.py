from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm, Booking, Room
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
from malabarhouse import settings
from django.http.response import JsonResponse, HttpResponse
from backend import colors
def google_calendar_url(self): #src=tie7uhbl3aohnfnuhotidikjpo%40group.calendar.google.com&color=%2342104A&src=nbc712s896fhv76pe8fl95o718%40group.calendar.google.com&color=%23125A12&src=vt8cbiploefrp3492ji1be25f0%40group.calendar.google.com&color=%236B3304&src=tcorkarb8uupa9nguqf9l2fbsc%40group.calendar.google.com&color=%238C500B&src=icoufgc83qm32aer4nuc3k9fjo%40group.calendar.google.com&color=%23865A5A&src=947tekb6h7nna597d11unjk1s8%40group.calendar.google.com&color=%23691426&src=nagh4bsa00ql8r2b4fiv0acnro%40group.calendar.google.com&color=%23853104&src=7gmv5vo3g01qbuneqh3tq4b4a4%40group.calendar.google.com&color=%2323164E&
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
    def google_calendar_url(self): #src=tie7uhbl3aohnfnuhotidikjpo%40group.calendar.google.com&color=%2342104A&src=nbc712s896fhv76pe8fl95o718%40group.calendar.google.com&color=%23125A12&src=vt8cbiploefrp3492ji1be25f0%40group.calendar.google.com&color=%236B3304&src=tcorkarb8uupa9nguqf9l2fbsc%40group.calendar.google.com&color=%238C500B&src=icoufgc83qm32aer4nuc3k9fjo%40group.calendar.google.com&color=%23865A5A&src=947tekb6h7nna597d11unjk1s8%40group.calendar.google.com&color=%23691426&src=nagh4bsa00ql8r2b4fiv0acnro%40group.calendar.google.com&color=%23853104&src=7gmv5vo3g01qbuneqh3tq4b4a4%40group.calendar.google.com&color=%2323164E&
        prefix = r"https://www.google.com/calendar/embed?title=Malabar%20House%20Bookings&height=600&wkst=1&bgcolor=%23FFFFFF&"
        suffix = r"ctz=America%2FLos_Angeles"
        color = 0
        for room in Room.objects.all():
            thiscal = "src="+room.request_cal_id.strip()+"&color=%23"+colors.CLUT[color][1]+"&"
            prefix += thiscal
        prefix += suffix
        return prefix
    def get_context_data(self, **kwargs):
        return {'rooms':Room.objects.all()}
        
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
