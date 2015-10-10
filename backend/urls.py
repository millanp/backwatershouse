from django.conf.urls import patterns, url, include
from backend import views
urlpatterns = patterns('', 
    url(r'^booking-submit', views.BookingCreate.as_view(), name='booking_submit'),
    #url(r'^paypal/', include('paypal.standard.ipn.urls'))
    url(r'^paypal/', views.paypal_processer, name='paypal-ipn'),
)