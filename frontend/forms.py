from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from backend.helpers import pretty_name
from dappr.forms import RegistrationForm


class PlaceholdersMixin(object):
    def __init__(self, *args, **kwargs):
        super(PlaceholdersMixin, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if isinstance(field.widget, forms.TextInput):
                    if field.label is not None:
                        field.widget.attrs['placeholder'] = unicode(field.label)
                    else:
                        field.widget.attrs['placeholder'] = unicode(pretty_name(field_name))
                    field.label = ""


class PrettyAuthenticationForm(PlaceholdersMixin, AuthenticationForm):
    pass


class PrettyPasswordResetForm(PlaceholdersMixin, PasswordResetForm):
    pass


class PrettyRegistrationForm(PlaceholdersMixin, RegistrationForm):
    pass


class PrettyPasswordSetForm(PlaceholdersMixin, SetPasswordForm):
    pass
