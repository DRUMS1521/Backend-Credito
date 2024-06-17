from app.accounting.models import Wallet, WalletMovement
from app.loans.models import Loan


def get_data_filler(user, date):
    user_wallet = Wallet.objects.get(user=user)
    movements = WalletMovement.objects.filter(wallet=user_wallet, created_at__date=date).order_by('id')
    total_income = 0
    initial_balance = movements.first().last_balance if movements.exists() else user_wallet.balance
    total_collected = 0
    total_loans = 0
    total_spend = 0
    final_balance = movements.last().last_balance if movements.exists() else user_wallet.balance




def get_pending_loans(user, date):
    user_loans = Loan.objects.filter(collector=user, is_finished=False)
    not_paid_loans = []
    paid_loans = []
    for loan in user_loans:
        pass
        