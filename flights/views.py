from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import SeatAvailability
from .forms import FlightForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Flight
from django.shortcuts import redirect
from .models import Reserva
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


def vuelos_disponibles(request):
    vuelos = Flight.objects.filter(is_active=True).order_by('departure_time')

    # Filtros
    airline = request.GET.get('airline')
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    fecha = request.GET.get('fecha')

    if airline:
        vuelos = vuelos.filter(airline__icontains=airline)
    if origin:
        vuelos = vuelos.filter(origin__icontains=origin)
    if destination:
        vuelos = vuelos.filter(destination__icontains=destination)
    if fecha:
        vuelos = vuelos.filter(departure_time__date=fecha)

    reservas = []
    if request.user.is_authenticated:
        reservas = Reserva.objects.filter(usuario=request.user)

    return render(request, 'vuelos_usuario.html', {
        'vuelos': vuelos,
        'reservas': reservas
    })


def listar_vuelos(request):
    vuelos = Flight.objects.all().order_by('-departure_time')
    return render(request, 'listar_vuelos.html', {'vuelos': vuelos})


def crear_vuelo(request):
    error = None
    exito = False
    autorizado = False
    vuelo_form = FlightForm()

    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        user = authenticate(username=username, password=password)

        if user and user.is_staff:
            autorizado = True

            if 'airline' in request.POST:  # Ahora sí validamos vuelo
                vuelo_form = FlightForm(request.POST)
                if vuelo_form.is_valid():
                    vuelo = vuelo_form.save(commit=False)
                    vuelo.created_by = user
                    vuelo.save()
                    SeatAvailability.objects.create(
                        flight=vuelo,
                        total_seats=vuelo_form.cleaned_data['total_seats'],
                        available_seats=vuelo_form.cleaned_data['total_seats']
                    )
                    vuelo_form = FlightForm()
                    exito = True
                else:
                    error = "Formulario inválido."
        else:
            error = "Usuario o contraseña incorrectos o no autorizado."

    return render(request, 'crear_vuelo.html', {
        'form': vuelo_form,
        'error': error,
        'exito': exito,
        'autorizado': autorizado
    })

@user_passes_test(lambda u: u.is_staff)
def editar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Flight, id=vuelo_id)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=vuelo)
        if form.is_valid():
            vuelo = form.save(commit=False)
            vuelo.created_by = request.user
            vuelo.save()
            return redirect('listar_vuelos')
    else:
        form = FlightForm(instance=vuelo)
    return render(request, 'crear_vuelo.html', {'form': form, 'autorizado': True})


def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('vuelo')

    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
        vuelo = reserva.vuelo
        disponibilidad = get_object_or_404(SeatAvailability, flight=vuelo)

        disponibilidad.available_seats += reserva.cantidad_asientos
        disponibilidad.save()
        reserva.delete()
        return redirect('mis_reservas')

    return render(request, 'mis_reservas.html', {'reservas': reservas})

@user_passes_test(lambda u: u.is_staff)
def eliminar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Flight, id=vuelo_id)
    if request.method == 'POST':
        vuelo.delete()
        return redirect('listar_vuelos')
    return redirect('listar_vuelos')

def reservar_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Flight, id=vuelo_id)
    disponibilidad = get_object_or_404(SeatAvailability, flight=vuelo)

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad_asientos', 1))
        except (ValueError, TypeError):
            cantidad = 1

        if cantidad <= 0:
            mensaje_error = "La cantidad debe ser mayor que cero."
        elif cantidad > disponibilidad.available_seats:
            mensaje_error = f"Solo hay {disponibilidad.available_seats} asiento(s) disponibles."
        else:
            # Crear reserva y descontar
            Reserva.objects.create(
                usuario=request.user,
                vuelo=vuelo,
                cantidad_asientos=cantidad
            )
            disponibilidad.available_seats -= cantidad
            disponibilidad.save()
            return redirect('vuelos_usuario')

        # Si hay error, renderizamos nuevamente
        vuelos = Flight.objects.filter(is_active=True).order_by('departure_time')
        reservas = Reserva.objects.filter(usuario=request.user)
        return render(request, 'vuelos_usuario.html', {
            'vuelos': vuelos,
            'mensaje_error': mensaje_error,
            'mensaje_error_vuelo_id': vuelo.id,
            'cantidad_enviada': cantidad
        })
    
    