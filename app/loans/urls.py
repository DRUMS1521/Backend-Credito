#urls
from django.urls import path
from .views import *

urlpatterns = [
    path('customer-loan', CustomerLoanAPIView.as_view(), name='customer-loan'),
    path('customers', CustomerBasicListAPIView.as_view(), name='customers'),
    path('all-customers', AllcustomersBasicListAPIView.as_view(), name='all-customers'),
    path('loans', LoanBasicListAPIView.as_view(), name='loans'),
    path('loans-full', LoanFullListAPIView.as_view(), name='loans-full'),
    path('<int:loan>/pay', CreatePaymentAPIView.as_view(), name='payments'),
    path('<int:pk>/order/<str:action>', UpdateLoanOrderingAPIView.as_view(), name='order'),
    path('markdowns/create', LoanMarkdownsCreateAPIView.as_view(), name='markdowns-create'),
    path('markdowns/list', LoanMarkdownsListAPIView.as_view(), name='markdowns-list'),
]