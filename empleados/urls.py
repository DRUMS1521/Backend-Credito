from django.urls import path
from empleados.views import EmpleadosListView, EmpleadoDetailView, EmpleadoUpdateRouteView

urlpatterns = [
    path('empleados', EmpleadosListView.as_view(), name='lista_empleados'),
    path('empleados/<int:pk>', EmpleadoDetailView.as_view(), name='detalle_empleado'),
    path('empleados/<int:pk>/update_route', EmpleadoUpdateRouteView.as_view(), name='update_route'),
]