from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from app.loans.serializers import CustomerBasicSerializer, CustomerCustomSerializer
from app.loans.models import Customer

class CustomerBasicListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerBasicSerializer
    pagination_class = None
    def get_queryset(self):
        return Customer.objects.filter(debt_collector=self.request.user)
    
class AllcustomersBasicListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerCustomSerializer
    pagination_class = None
    def get_queryset(self):
        return Customer.objects.all()