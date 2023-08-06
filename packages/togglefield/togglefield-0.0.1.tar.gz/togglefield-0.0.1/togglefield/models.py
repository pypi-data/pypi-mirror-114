from togglefield.widgets import ToggleSwitchWidget
from togglefield.forms import ToggleSwitchFormField
from django.db import models # noqa


class ToggleSwitchField(models.BooleanField):
    default_error_messages = {
        'invalid': ("'%s' is not a Boolean.")
    }

    def __init__(self, *args, **kwargs):
        super(ToggleSwitchField, self).__init__(*args, **kwargs)
        self.validate(self.get_default(), None)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': ToggleSwitchFormField,
            'widget': ToggleSwitchWidget
        }
        defaults.update(**kwargs)
        return super(ToggleSwitchField, self).formfield(**defaults)
