from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('crear-vuelo/', views.crear_vuelo, name='crear_vuelo'),
    path('vuelos/', views.listar_vuelos, name='listar_vuelos'),
    path('editar-vuelo/<int:vuelo_id>/', views.editar_vuelo, name='editar_vuelo'),
    path('eliminar-vuelo/<int:vuelo_id>/', views.eliminar_vuelo, name='eliminar_vuelo'),
    path('usuario/vuelos/', views.vuelos_disponibles, name='vuelos_usuario'),
    path('usuario/reservas/', views.mis_reservas, name='mis_reservas'),
    path('usuario/reservar/<int:vuelo_id>/', views.reservar_vuelo, name='reservar_vuelo'),
]