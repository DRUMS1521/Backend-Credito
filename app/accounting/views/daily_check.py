from app.accounting.serializers import DailyCheckoutSerializer, DailyCheckoutFillerSerializer
from rest_framework import generics
from app.accounting.models import DailyCheckout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.accounting.helpers import get_data_filler
from django.utils import timezone


class DailyCheckoutListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyCheckoutSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = DailyCheckout.objects.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyCheckoutFillerView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DailyCheckoutFillerSerializer

    def get(self, request):
        today = timezone.now().date()
        if DailyCheckout.objects.filter(user=request.user, created_at__date=today).exists():
            return Response({'message': 'Ya has hecho un cierre de caja hoy'}, status=status.HTTP_400_BAD_REQUEST)
        data = get_data_filler(request.user, today)
        serializer = DailyCheckoutFillerSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

        