from app.accounting.models import Wallet, WalletMovement
from app.loans.models import Loan, Payment
from django.db.models import Sum


def get_data_filler(user, date):
    user_wallet = Wallet.objects.get(user=user)
    movements = WalletMovement.objects.filter(wallet=user_wallet, created_at__date=date).order_by('id')
    # Total income refers to the total amount of money that has entered the wallet with type 'entry' or 'admin_charge'
    total_income = movements.filter(type__in=['entry', 'admin_charge']).aggregate(total_income=Sum('amount'))['total_income'] or 0
    initial_balance = movements.first().last_balance if movements.exists() else user_wallet.balance
    # Total collected refers to the total amount of money that has left the wallet with type 'loan_in' - 'loan_out'
    total_collected = movements.filter(type__in=['loan_in', 'loan_out']).aggregate(total_collected=Sum('amount'))['total_collected'] or 0
    total_loans = Loan.objects.filter(collector=user, created_at__date=date).aggregate(total_loans=Sum('amount'))['total_loans'] or 0
    total_spend = movements.filter(type='exit').aggregate(total_spend=Sum('amount'))['total_spend'] or 0
    final_balance = movements.last().current_balance if movements.exists() else user_wallet.balance
    user_loans = Loan.objects.filter(collector=user, is_finished=False)
    loans_in_arrears = 0
    loans_in_arrears_amount = 0
    for loan in user_loans:
        days_in_arrears, dues_in_arrears, amount_in_arrears = loan.get_arrears()
        if days_in_arrears > 0:
            loans_in_arrears += 1
            loans_in_arrears_amount += amount_in_arrears
    # Count distinct Loan on Payment
    loans_paid = Payment.objects.filter(loan__collector=user, created_at__date=date).values('loan').distinct().count()
    return {
        'initial_balance': initial_balance,
        'total_income': total_income,
        'total_collected': total_collected,
        'total_loans': total_loans,
        'total_spend': total_spend,
        'final_balance': final_balance,
        'loans_in_arrears_amount': loans_in_arrears_amount,
        'loans_in_arrears': loans_in_arrears,
        'loans_paid': loans_paid
    }