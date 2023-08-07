from django.urls import path
from empleados.views import EmpleadosListView, EmpleadoDetailView

urlpatterns = [
    path('empleados', EmpleadosListView.as_view(), name='lista_empleados'),
    path('empleados/<int:pk>', EmpleadoDetailView.as_view(), name='detalle_empleado'),
]