from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'frontend/gateway.html'}),
    url(r'^$', include("frontend.urls")),
    # url(r'^blog/', include('blog.urls')),
    #url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
