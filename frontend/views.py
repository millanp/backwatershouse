from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import BookingForm, Booking
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
from malabarhouse import settings
from django.http.response import JsonResponse, HttpResponse
class BookingCreate(CreateView, LoginRequiredMixin):
    form_class = BookingForm
    success_url = '/booking'
    template_name = 'frontend/booking.html'
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.guest = self.request.user
        obj.save()
        super(CreateView, self).form_valid(form)
        return JsonResponse({"FOO":"FFFFFS"})
    def form_invalid(self, form):
        return HttpResponse(form.as_p())
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
