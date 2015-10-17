from django.conf.urls import patterns, include, url
from django.contrib import admin
import django.contrib.auth.views as djviews
urlpatterns = patterns('',
    # Examples:
    url('^', include('django.contrib.auth.urls')),
    # url(r'^blog/', include('blog.urls')),
    #url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
