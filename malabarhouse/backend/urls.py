from django.conf.urls import patterns, url
import views
urlpatterns = patterns('', 
    url(r'^booking-submit', views.BookingCreate.as_view(), name='booking_submit')
)