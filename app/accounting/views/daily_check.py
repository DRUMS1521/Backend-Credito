from app.accounting.serializers import DailyCheckoutSerializer
from rest_framework import generics
from app.accounting.models import DailyCheckout
from rest_framework.permissions import IsAuthenticated


class DailyCheckoutListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyCheckoutSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = DailyCheckout.objects.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)