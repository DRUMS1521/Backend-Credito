from app.loans.models import Loan
from app.accounting.models import WalletMovement, Wallet
from app.loans.serializers import LoanBasicSerializer, FullLoanSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

class LoanDestroyAPIView(DestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanBasicSerializer
    permission_classes = (IsAdminUser,)

    def perform_destroy(self, instance):
        # Regenerate wallet movements
        principal_amount_paid = instance.principal_amount_paid
        interest_amount_paid = instance.interest_amount_paid
        total_paid = principal_amount_paid + interest_amount_paid
        loan_amount = instance.amount
        user_wallet = Wallet.objects.get(user=instance.collector)
        WalletMovement.objects.create(
            wallet=user_wallet,
            type='positive_delete_loan',
            amount=loan_amount,
            name='Cancelación de préstamo',
            reason=f'Cancelación de préstamo {instance.id}'
        )
        WalletMovement.objects.create(
            wallet=user_wallet,
            type='negative_delete_loan',
            amount=total_paid,
            name='Cancelación de préstamo',
            reason=f'Cancelación de préstamo {instance.id}'
        )
        instance.delete()

class LoanBasicListAPIView(ListAPIView):
    serializer_class = LoanBasicSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        user = self.request.user
        query = Loan.objects.all()
        collector = self.request.query_params.get('user', None)
        # Search date from query params
        date = self.request.query_params.get('date', None)
        if date is not None:
            query =  query.filter(created_at__date=date)
        if user.is_superuser or user.is_staff:
            if collector is not None and collector != '' and collector != '0' and collector !=0 and collector!='all':
                query = query.filter(collector__id=collector)
            else:
                query = query.filter(collector=user)
        else:
            query = query.filter(collector=user)
        return query.order_by('-id')
        

        
class LoanFullListAPIView(ListAPIView):
    serializer_class = FullLoanSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # View as other user
            user_id = self.request.query_params.get('user', None)
            if user_id is not None and user_id != '':
                user = user_id
            else:
                user_id = user.id
        else:
            user_id = user.id

        now = timezone.now()
        case_1 = Q(is_finished=False)
        case_2 = Q(is_finished=True, finished_at__gte=now - timedelta(hours=12))
        combined_cases = case_1 | case_2
        # search by customer name
        customer_name = self.request.query_params.get('customer_name', None)
        if customer_name is not None and customer_name != '':
            combined_cases &= Q(customer__name__icontains=customer_name)
        return Loan.objects.filter(combined_cases, collector__id=user_id).order_by('ordering', '-id')

