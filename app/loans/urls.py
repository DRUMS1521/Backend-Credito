#urls
from django.urls import path
from .views import *

urlpatterns = [
    path('customer-loan', CustomerLoanAPIView.as_view(), name='customer-loan'),
    path('customers', CustomerBasicListAPIView.as_view(), name='customers'),
    path('customers/<int:pk>/details', AllcustomersFullRetrieveAPIView.as_view(), name='all-customers'),
    path('loans', LoanBasicListAPIView.as_view(), name='loans'),
    path('loans-full', LoanFullListAPIView.as_view(), name='loans-full'),
    path('<int:pk>', LoanDestroyAPIView.as_view(), name='loan-delete'),
    path('<int:loan>/pay', CreatePaymentAPIView.as_view(), name='payments'),
    path('<int:pk>/order/<str:action>', UpdateLoanOrderingAPIView.as_view(), name='order'),
    path('order', CustomUpdateOrderingLoanAPIView.as_view(), name='custom-order'),
    path('markdowns/create', LoanMarkdownsCreateAPIView.as_view(), name='markdowns-create'),
    path('markdowns/list', LoanMarkdownsListAPIView.as_view(), name='markdowns-list'),
    path('customers/add-notes', CustomerAddNotesAPIView.as_view(), name='add-notes'),
    path('customers/<int:pk>', EditCustomerAPIView.as_view(), name='edit-customer'),
]