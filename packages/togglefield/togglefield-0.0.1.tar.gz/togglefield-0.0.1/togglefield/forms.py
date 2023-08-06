from togglefield.widgets import ToggleSwitchWidget
from django import forms


class ToggleSwitchFormField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = ToggleSwitchWidget
        super(ToggleSwitchFormField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if value in self.empty_values and self.required:
            raise forms.ValidationError(
                self.error_messages["required"], code="required"
            )
