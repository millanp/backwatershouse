from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'malabarhouse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
