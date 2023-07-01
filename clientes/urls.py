from django.urls import path
from clientes.views import ClientesListView, ClienteDetailView, ClienteCreateView

urlpatterns = [
    path('clientes/', ClientesListView.as_view(), name='lista_clientes'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    path('clientes/create/', ClienteCreateView.as_view(), name='crear_cliente'),

]