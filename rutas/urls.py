from django.urls import path
from rutas.views.basics import RutasListView, RutasDetailView

urlpatterns = [
    path('rutas', RutasListView.as_view(), name='lista_rutas'),
    path('rutas/<int:pk>', RutasDetailView.as_view(), name='detalle_ruta'),
]
