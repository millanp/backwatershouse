from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import urls as authurls
from django.contrib.auth import views as authviews
from dappr import urls as dapprurls
from frontend import forms

admin.site.site_header = "%s Administration" % (settings.VENUE_NAME)

base_login_context = {
    "venue_name": settings.VENUE_NAME,
}

urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', authviews.logout_then_login, name='logout'),
    url('^accounts/login/', authviews.login, {'authentication_form': forms.PrettyRegistrationForm}),
    url('^accounts/', include(authurls), {"extra_context":base_login_context}),
    url('^r/', include(dapprurls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
