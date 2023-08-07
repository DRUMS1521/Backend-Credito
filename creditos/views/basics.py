from rest_framework import generics 
from rest_framework.response import Response
from creditos.models import Creditos
from creditos.serializers.basics import CreditoSerializer
from rest_framework import permissions
from django.db.models import Q


class ListaCreditosView(generics.ListCreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        finalizado = self.request.query_params.get('finalizado', None)
        if finalizado == 'true':
            queryset = queryset.filter(Q(credito_finalizado=True))
        else:
            pass
        return queryset


class DetalleCreditoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]  

class CreditoCreateView(generics.CreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]