# django-togglefield
Simple library to enable togglefield in Django

How to enable the app:

1. Install the library from `Github`
```python
pip install git+https://github.com/mattiagiupponi/django-togglefield.git@master
```
2. Enable the app in your Django Project by adding it into the `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ....,
    'togglefield',
    ....
]
```
3. Define the field into your form:

```python
from django.forms import forms
from togglefield.forms import ToggleSwitchFormField

class FormWithToggle(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    toggle = ToggleSwitchFormField(required=False)
```
4. Render your form in your html page:

views.py
```python
def index(request):
    context = {
        "form": FormWithToggle
    }
    return render(request, 'app/index.html', context)

```
index.html
```
{{form.as_p}}
```

5. Enjoi your field

