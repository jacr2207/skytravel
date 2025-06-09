from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    total_seats = forms.IntegerField(min_value=1)
    price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)

    class Meta:
        model = Flight
        fields = ['airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'price']