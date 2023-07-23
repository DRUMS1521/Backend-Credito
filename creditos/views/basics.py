from rest_framework import generics 
from rest_framework.response import Response
from creditos.models import Creditos
from creditos.serializers.basics import CreditoSerializer


class ListaCreditosView(generics.ListCreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer

class DetalleCreditoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer

class CreditoCreateView(generics.CreateAPIView):
    queryset = Creditos.objects.all()
    serializer_class = CreditoSerializer