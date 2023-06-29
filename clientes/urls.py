from django.urls import path
from clientes.views import *

urlpatterns = [
    path('clientes/', ClientesListView.as_view(), name='lista_clientes'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    # Agrega más URLs y vistas según tus necesidades.
]
