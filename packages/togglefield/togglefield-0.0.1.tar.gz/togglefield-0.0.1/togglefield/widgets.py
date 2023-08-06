from django.forms.widgets import Input


class ToggleSwitchWidget(Input):
    input_type = 'checkbox'
    template_name = 'toggle/toggle.html'

    def render(self, name, value, attrs=None, renderer=None):
        return super(ToggleSwitchWidget, self).\
            render(name, value, attrs, renderer)
