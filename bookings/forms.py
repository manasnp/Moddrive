from django import forms

from fleet.models import DrivingRoute
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'route', 'customer_notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'customer_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes for staff'}),
        }

    def __init__(self, *args, vehicle=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vehicle = vehicle
        self.fields['route'].required = False
        if vehicle:
            compatible = vehicle.routes.all()
            self.fields['route'].queryset = compatible if compatible.exists() else DrivingRoute.objects.all()


class BookingDecisionForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'decision_reason']
        widgets = {'decision_reason': forms.Textarea(attrs={'rows': 4})}
