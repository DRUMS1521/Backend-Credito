from rest_framework import generics
from finanzas.models.finanzas import Finanzas
from finanzas.serializers.basics import FinanzasSerializer

class FinanzasListView(generics.ListCreateAPIView):
    queryset = Finanzas.objects.all()
    serializer_class = FinanzasSerializer

class FinanzasDetailView(generics.RetrieveUpdateAPIView):
    queryset = Finanzas.objects.all()
    serializer_class = FinanzasSerializer
