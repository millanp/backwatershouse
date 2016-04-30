from django.contrib.auth.forms import AuthenticationForm
from django import forms

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
