from backend.models import BookingForm, Booking, Room
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from django.views.generic.edit import CreateView
from backend import colors
from django.conf import settings
# Using the list of Room instances, generate a URL for the embedded calendar
# that incorporates all request calendars and all booking calendars into one


def google_calendar_url():
    cal_title = "%s Bookings" % settings.VENUE_NAME
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

#         return JsonResponse(form.errors, status=400)
# Create your views here.
class InnerPageContextMixin(object):
    context = {}    
    base_context = {
        "venue_name": settings.VENUE_NAME
    }

    def get_context_data(self, **kwargs):
        final_context = self.base_context.copy()
        final_context.update(self.context)
        return final_context

class InnerPageView(LoginRequiredMixin, InnerPageContextMixin, TemplateView):
    template_name = "frontend/home.html"

class MyVisitsView(InnerPageView):
    template_name = "frontend/requests.html"
    context = {}

    def get_context_data(self, **kwargs):
        previous_context = super(MyVisitsView, self).get_context_data(**kwargs)
        final_context = self.context.copy()
        added_context = {'bookings': Booking.objects.filter(guest=self.request.user)}
        final_context.update(added_context)
        final_context.update(previous_context)
        return final_context

class BookingCreate(LoginRequiredMixin, InnerPageContextMixin, FormValidMessageMixin, CreateView):
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
    form_valid_message = 'Request sent to administrator'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.guest = self.request.user
        obj.save()
        return super(BookingCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        innerpage_context = InnerPageContextMixin.get_context_data(self, **kwargs)
        createview_context = CreateView.get_context_data(self, **kwargs)
        createview_context['cal_url'] = google_calendar_url()
        createview_context.update(innerpage_context)
        return createview_context
