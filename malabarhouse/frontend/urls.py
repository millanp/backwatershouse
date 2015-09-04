from django.conf.urls import patterns, url, include
from frontend import views
from frontend.views import TemplateViewPlus, requestsView
from backend.models import BookingForm, Booking
from django.views.generic.edit import FormView
urlpatterns = patterns('',
    url(r'^registration/', include('registration.urls')),
    url(r'^booking/', views.BookingCreate.as_view(), name='booking'),
    url(r'^my-visits/', requestsView, name='requests'),
    url(r'^$', TemplateViewPlus.as_view(template_name='frontend/home.html'), name='home'),
)