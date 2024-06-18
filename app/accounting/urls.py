from django.urls import path
from .views import *

urlpatterns = [
    path('spends', SpendListCreateAPIView.as_view(), name='spends'),
    path('spends/<int:pk>', DeleteSpendAPIView.as_view(), name='spends'),
    #Deposits
    path('deposits', DepositListCreateAPIView.as_view(), name='deposits'),
    #Wallet
    path('wallet', WalletCheckerAPIView.as_view(), name='deposits'),
    #Daily checkout
    path('daily-checkout', DailyCheckoutListCreateView.as_view(), name='daily-checkout'),
    path('daily-checkout-filler', DailyCheckoutFillerView.as_view(), name='daily-checkout-filler'),
    #Period closures
    path('period-closures', PeriodClosuresListCreateView.as_view(), name='period-closures'),
    path('period-closures/<int:pk>', PeriodClosuresRetrieveUpdateAPIView.as_view(), name='period-closures'),
    path('actual-period-closure', ActualPeriodClosureRetrieveAPIView.as_view(), name='actual-period-closure'),
    path('period-closure-custom', PeriodClosureCustomCreateView.as_view(), name='period-closure-custom'),
]