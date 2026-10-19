from django import forms
from .models import Vehicle

class VehicleFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search by name or manufacturer", "class": "form-control"}),
    )

    vehicle_type = forms.ChoiceField(
        required=False,
        label="Vehicle Type",
        choices=[("", "All types")] + list(Vehicle.VEHICLE_TYPES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    transmission = forms.ChoiceField(
        required=False,
        label="Transmission",
        choices=[("", "All transmissions")] + list(Vehicle.TRANSMISSION_TYPES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    maximum_price = forms.DecimalField(
        required=False,
        label="Maximum daily price",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Maximum price", "class": "form-control"}),
    )