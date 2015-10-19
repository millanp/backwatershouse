from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls, views
urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', views.logout_then_login, name='logout'),
    url('^accounts/', include(urls)),
    # url(r'^blog/', include('blog.urls')),
    #url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
