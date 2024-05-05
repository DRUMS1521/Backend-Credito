from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from app.loans.serializers import CustomerBasicSerializer, CustomerCustomSerializer, CustomerAddNotesSerializer
from app.loans.models import Customer

class CustomerBasicListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerBasicSerializer
    pagination_class = None
    def get_queryset(self):
        queryset = Customer.objects.all()
        # get filter params
        name = self.request.query_params.get('name', None)
        phone = self.request.query_params.get('phone', None)
        document_like = self.request.query_params.get('document_like', None)
        document = self.request.query_params.get('document', None)
        debt_collector = self.request.query_params.get('debt_collector', None)
        if name is not None and name != '' and name != 'null':
            queryset = queryset.filter(name__icontains=name)
        if phone is not None and phone != '' and phone != 'null':
            queryset = queryset.filter(phone__icontains=phone)
        if document_like is not None and document_like != '' and document_like != 'null':
            queryset = queryset.filter(document_number__icontains=document_like)
        if document is not None and document != '' and document != 'null':
            queryset = queryset.filter(document_number=document)
        if debt_collector is not None and debt_collector != '' and debt_collector != 'null' and debt_collector != 'all':
            queryset = queryset.filter(debt_collector__id=debt_collector)
        return queryset
    
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