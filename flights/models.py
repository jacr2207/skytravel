from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Flight(models.Model):
    airline = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # para cancelación futura

    def __str__(self):
        return f"{self.origin} a {self.destination} - {self.departure_time}"

class SeatAvailability(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Asientos para vuelo {self.flight.id}"

class Reserva(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vuelo = models.ForeignKey(Flight, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    cantidad_asientos = models.PositiveIntegerField(default=1)  # 👈 nuevo campo

    def __str__(self):
        return f"{self.usuario.email} - {self.vuelo} ({self.cantidad_asientos} asientos)"