from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import views as authurls
from dappr import urls as dapprurls

admin.site.site_header = "Malabar House Administration"
urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', views.logout_then_login, name='logout'),
    url('^accounts/', include(authurls)),
    url('^r/', include(dapprurls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
