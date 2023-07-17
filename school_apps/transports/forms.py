from django import forms
from school_apps.transports.models import Transport


class TransportForm(forms.ModelForm):
    no_of_vehicle = forms.CharField(
        label="Number of Vehicle",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Number of Vehicle",
            }
        ),
    )
    route_fare = forms.DecimalField(
        label="Route Fare",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Transport Fee/Month",
            }
        ),
    )
    route_name = forms.CharField(
        label="Route Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Destination1 - Destination2",
            }
        ),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "cols": 10,
                "placeholder": " Enter  Transport Description",
            }
        ),
    )
    driver_name = forms.CharField(
        required=False,
        label="Driver Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-inline",
                "placeholder": "Enter Driver Name",
            }
        ),
    )

    class Meta:
        model = Transport
        fields = "__all__"
