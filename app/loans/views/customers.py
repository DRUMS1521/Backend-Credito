from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from app.loans.serializers import CustomerBasicSerializer, CustomerCustomSerializer, CustomerAddNotesSerializer
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
    
class CustomerAddNotesAPIView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CustomerAddNotesSerializer
    queryset = Customer.objects.all()

class EditCustomerAPIView(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CustomerBasicSerializer
    queryset = Customer.objects.all()