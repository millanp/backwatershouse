from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from braces.forms import Success
from django import forms
from dappr.forms import RegistrationForm

class PlaceholdersInsteadOfLabelsMixin(object):
    def __init__(self, *args, **kwargs):
        super(PlaceholdersInsteadOfLabelsMixin, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if isinstance(field.widget, forms.TextInput):
                    field.widget.attrs['placeholder'] = field.label
                    field.label = ""


class PrettyAuthenticationForm(PlaceholdersInsteadOfLabelsMixin, AuthenticationForm):
    pass


class PrettyPasswordResetForm(PlaceholdersInsteadOfLabelsMixin, PasswordResetForm):
    pass


class PrettyRegistrationForm(PlaceholdersInsteadOfLabelsMixin, RegistrationForm):
    pass