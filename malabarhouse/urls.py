from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls
urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'template_name': 'admin/login.html'}),
    url('^', include(urls)),
    # url(r'^blog/', include('blog.urls')),
    #url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
