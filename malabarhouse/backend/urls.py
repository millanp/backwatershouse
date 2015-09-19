from django.conf.urls import patterns, url, include
import views
urlpatterns = patterns('', 
    url(r'^booking-submit', views.BookingCreate.as_view(), name='booking_submit'),
    url(r'^paypal/', include('paypal.standard.ipn.urls'))
)