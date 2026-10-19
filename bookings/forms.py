from django import forms

from fleet.models import DrivingRoute

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "route",
            "start_date",
            "end_date",
            "customer_notes",
        ]

    widgets = {
        "route": forms.Select(attrs={"class": "form-control"}),
        "start_date": forms.DateInput(attrs={"type": "date"}),
        "end_date": forms.DateInput(attrs={"type": "date"}),
        "customer_notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    }

    labels = {
        "route": "Select Driving Route (optional)",
        "start_date": "RentalStart Date",
        "end_date": "Rental End Date",
        "customer_notes": "Additional Notes",
    }

def __init__(self, *args, vehicle=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["route"].required = False
    self.vehicle = vehicle

    if vehicle:
        self.fields["route"].queryset = DrivingRoute.objects.filter(vehicle=vehicle)
    else:
        self.fields["route"].queryset = DrivingRoute.objects.none()

class BookingDecisionForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status"]

    widgets = {
        "status": forms.Select(attrs={"class": "form-control"}),
    }

    labels = {
        "status": "Booking Status",
    }

    
        
