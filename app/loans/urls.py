#urls
from django.urls import path
from .views import *

urlpatterns = [
    path('customer-loan', CustomerLoanAPIView.as_view(), name='customer-loan'),
    path('customers', CustomerBasicListAPIView.as_view(), name='customers'),
    path('loans', LoanBasicListAPIView.as_view(), name='loans'),
    path('loans-full', LoanFullListAPIView.as_view(), name='loans-full'),
    path('<int:loan>/pay', CreatePaymentAPIView.as_view(), name='payments'),
]