from django.conf.urls import patterns, url, include
from frontend import views
from backend.models import BookingForm, Booking, Room
from django.views.generic.edit import FormView
urlpatterns = patterns('',
    url(r'^booking/', views.BookingCreate.as_view(), name='booking'),
    url(r'^my-visits/', views.MyVisitsView.as_view(), name='requests'),
    url(r'^rooms/', views.InnerPageView.as_view(template_name='frontend/rooms.html', 
                                                   context={'rooms':Room.objects.all()}),
        name='rooms'),
    url(r'^$', views.InnerPageView.as_view(template_name='frontend/home.html'), name='home'),
)