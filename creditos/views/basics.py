from rest_framework import generics 
from rest_framework.response import Response
from creditos.models import Creditos
from creditos.serializers.basics import CreditoSerializer
from rest_framework import permissions


class ListaCreditosView(generics.ListCreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

class DetalleCreditoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]  

class CreditoCreateView(generics.CreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]  