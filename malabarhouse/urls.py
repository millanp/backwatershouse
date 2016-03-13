from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth
import dappr

admin.site.site_header = "Malabar House Administration"
urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', auth.views.logout_then_login, name='logout'),
    url('^accounts/', include(auth.urls)),
    url('^r/', include(dappr.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
