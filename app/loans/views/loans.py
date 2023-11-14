from app.loans.models import Loan
from app.loans.serializers import LoanBasicSerializer, FullLoanSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class LoanBasicListAPIView(ListAPIView):
    serializer_class = LoanBasicSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        # Search date from query params
        date = self.request.query_params.get('date', None)
        if date is not None:
            return Loan.objects.filter(created_at__date=date, customer__debt_collector = self.request.user)
        else:
            return Loan.objects.filter(customer__debt_collector = self.request.user)
        
class LoanFullListAPIView(ListAPIView):
    serializer_class = FullLoanSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        if self.request.user.is_superuser:
            # View as other user
            user = self.request.query_params.get('user', None)
            if user is not None and user != '':
                return Loan.objects.filter(customer__debt_collector__id=user).order_by('ordering')
            else:
                return Loan.objects.filter(customer__debt_collector = self.request.user).order_by('ordering')
        return Loan.objects.filter(customer__debt_collector = self.request.user).order_by('ordering')