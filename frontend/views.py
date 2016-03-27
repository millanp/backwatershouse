from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm, Booking, Room
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http.response import HttpResponse
from backend import colors

# Using the list of Room instances, generate a URL for the embedded calendar
# that incorporates all request calendars and all booking calendars into one
def google_calendar_url():
    cal_title = "Malabar House Bookings"
    cal_title = cal_title.replace(" ", "%20")
    prefix = (r"https://www.google.com/calendar/embed"
              r"?title=cal_title"
              r"&height=600&wkst=1&bgcolor=%23FFFFFF&")
    prefix = prefix.replace("cal_title", cal_title)
    suffix = r"ctz=America%2FLos_Angeles"
    color = 0
    for room in Room.objects.all():
        thiscal = ("src="+room.request_cal_id.strip()+
                   "&color=%23"+colors.COLORS[color]+
                   "&src="+room.booking_cal_id.strip()+
                   "&color=%23"+colors.COLORS[color+1]+"&")
        prefix += thiscal
        color += 2
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

    def get_context_data(self, **kwargs):
        dic = CreateView.get_context_data(self, **kwargs)
        dic['cal_url'] = google_calendar_url()
        return dic

#         return JsonResponse(form.errors, status=400)
# Create your views here.


class TemplateViewPlus(LoginRequiredMixin, TemplateView):
    template_name = "frontend/home.html"
    context = {}

    def get_context_data(self, **kwargs):
        return self.context


@login_required
def requestsView(request):
    print 'displaying requests'
    return render(
        request,
        'frontend/requests.html',
        {'bookings': Booking.objects.filter(guest=request.user)})
