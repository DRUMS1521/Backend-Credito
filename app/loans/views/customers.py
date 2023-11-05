from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from app.loans.serializers import CustomerBasicSerializer
from app.loans.models import Customer

class CustomerBasicListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerBasicSerializer
    pagination_class = None


    def get_queryset(self):
        return Customer.objects.filter(debt_collector=self.request.user)