from django.conf.urls import patterns, url, include
from frontend import views
urlpatterns = patterns('',
    url(r'^registration/', include('registration.urls')),
    url(r'^booking/', views.booking, name='booking'),
    url(r'^$', views.home, name='home'),
)