from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django.contrib.auth.models import User
from .models import City
from tempus_dominus.widgets import DatePicker
from datetime import datetime

date = datetime.now().date().strftime('%Y-%m-%d')


class DestinationForm(forms.Form):
    from_city = forms.ModelChoiceField(queryset=City.objects.all().order_by('name'), empty_label='Select from')
    to_city = forms.ModelChoiceField(queryset=City.objects.all().order_by('name'), empty_label='Select to')

    date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': date,
                'maxDate': '2023-12-31',
            },
        ),
        initial=date
    )
    passengers = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Div(
                Div(
                    'from_city',
                    css_class="d-flex align-items-center flex-fill me-sm-1 my-sm-0 my-4 border-bottom position-relative"
                ),
                Div(
                    'to_city',
                    css_class='d-flex align-items-center flex-fill ms-sm-1 my-sm-0 my-4 border-bottom position-relative'
                ),
                css_class="form-group d-sm-flex margin"
            ),
            Div(
                Div(
                    'date',
                    css_class='d-flex align-items-center flex-fill me-sm1 my-sm-0 border-bottom position-relative'
                ),
                css_class='form-group d-sm-flex margin'
            ),
            Div(
                'passengers',
                css_class='form-group border-bottom d-flex align-items-center position-relative'
            ),
            Div(
                Div(
                    Submit(
                        'submit', 'Search Flights',
                        css_class="btn btn-primary rounded-0 d-flex justify-content-center text-center p-3"
                    ),
                    css_class='d-grid gap-2'
                ),
                css_class='form-group my-3'
            )
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

