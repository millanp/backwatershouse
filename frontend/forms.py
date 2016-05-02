from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django import forms
from django.forms.utils import pretty_name
from dappr.forms import RegistrationForm


class PlaceholdersInsteadOfLabelsMixin(object):
    def __init__(self, *args, **kwargs):
        super(PlaceholdersInsteadOfLabelsMixin, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if isinstance(field.widget, forms.TextInput):
                    if field.label is not None:
                        field.widget.attrs['placeholder'] = unicode(field.label)
                    else:
                        field.widget.attrs['placeholder'] = unicode(pretty_name(field.name))
                    field.label = ""


class PrettyAuthenticationForm(PlaceholdersInsteadOfLabelsMixin, AuthenticationForm):
    pass


class PrettyPasswordResetForm(PlaceholdersInsteadOfLabelsMixin, PasswordResetForm):
    pass


class PrettyRegistrationForm(PlaceholdersInsteadOfLabelsMixin, RegistrationForm):
    pass