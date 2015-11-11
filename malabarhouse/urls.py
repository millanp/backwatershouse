from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls, views
from registration.forms import RegistrationFormUniqueEmail
from registration.views import RegistrationView
class RegistrationViewUniqueEmail(RegistrationView):
    form_class=RegistrationFormUniqueEmail
urlpatterns = patterns('',
    # Examples:
    url('^accounts/logout/', views.logout_then_login, name='logout'),
    url('^accounts/', include(urls)),
#     url(r'^registration/register/$', RegistrationViewUniqueEmail.as_view(), name="myregistration_register"),
    url(r'^registration/', include('registration.urls')),
    # url(r'^blog/', include('blog.urls')),
    #url('^registration/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backend/', include("backend.urls")),
    url(r'^', include("frontend.urls")),
)
