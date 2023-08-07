from rest_framework import generics 
from rest_framework.response import Response
from creditos.models import Creditos, Payments
from empleados.models import Empleados
from rutas.models import Rutas
from creditos.serializers.payments import PaymentsSerializer, PaymentsDetailSerializer
from rest_framework import permissions
from django.db.models import Q
from django.utils import timezone
import pdb

class ListPaymentsView(generics.ListAPIView):
    queryset = Payments.objects.all().order_by('id')
    serializer_class = PaymentsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = Payments.objects.all().order_by('id')
        #pdb.set_trace()
        user = self.request.user
        if user.is_superuser:
            query_date = self.request.query_params.get('date', None)
            query_ruta = self.request.query_params.get('ruta', None)
            query_solo_pendientes = self.request.query_params.get('only_pending', None)
            if query_date is not None and query_date != '':
                #use Q to filter the main queryset
                queryset = queryset.filter(Q(fecha_pago=query_date))
            if query_ruta is not None and query_ruta != '':
                #use Q to filter the main queryset
                queryset = queryset.filter(Q(ruta=query_ruta))
            if query_solo_pendientes == 'true':
                queryset = queryset.filter(Q(credito_finalizado=False))
        else:
            try:
                empleado = Empleados.objects.get(user=user)
            except:
                queryset = Payments.objects.none()
            try:
                ruta = Rutas.objects.get(id_empleado=empleado)
            except:
                queryset = Payments.objects.none()
            else:
                queryset = Payments.objects.filter(ruta=ruta, fecha_pago=timezone.now(), credito__credito_finalizado=False).order_by('id')
        return queryset
    
class UpdatePaymentsView(generics.UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]
