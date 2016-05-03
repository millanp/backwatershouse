from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import urls as authurls
from django.contrib.auth import views as authviews
from dappr import urls as dapprurls
from dappr import views as dapprviews
from frontend import forms

admin.site.site_header = "%s Administration" % (settings.VENUE_NAME)

base_login_context = {
    "venue_name": settings.VENUE_NAME,
}

urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', authviews.logout_then_login, name='logout'),
    url('^accounts/login/', authviews.login,
        {'authentication_form': forms.PrettyAuthenticationForm}, name='login'),
    url('^accounts/password_reset', authviews.password_reset,
        {'password_reset_form': forms.PrettyPasswordResetForm}, name='password_reset'),
    url('^accounts/', include(authurls), {"extra_context": base_login_context}),
    url('^r/register', 
        dapprviews.RegistrationForm.as_view(form_class=forms.PrettyRegistrationForm),
        name='register'),
    url(r'confirm/(?P<conf_key>[0-9]+)', 
        dapprviews.UserPasswordUpdate.as_view(form_class=forms.PrettyPasswordSetForm), 
        name='confirmation_view'),
    url('^r/', include(dapprurls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
