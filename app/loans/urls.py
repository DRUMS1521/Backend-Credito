#urls
from django.urls import path
from .views import *

urlpatterns = [
    path('customer-loan', CustomerLoanAPIView.as_view(), name='customer-loan'),
    path('customers', CustomerBasicListAPIView.as_view(), name='customers'),
    path('loans', LoanBasicListAPIView.as_view(), name='loans'),
]