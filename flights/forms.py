from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    total_seats = forms.IntegerField(min_value=1)

    class Meta:
        model = Flight
        fields = ['airline', 'origin', 'destination', 'departure_time', 'arrival_time']