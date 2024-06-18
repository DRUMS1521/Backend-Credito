from .customer_loan import CustomerLoanAPIView
from .customers import CustomerBasicListAPIView, AllcustomersFullRetrieveAPIView, CustomerAddNotesAPIView, EditCustomerAPIView
from .loans import LoanBasicListAPIView, LoanFullListAPIView, LoanDestroyAPIView
from .payments import CreatePaymentAPIView
from .ordering import UpdateLoanOrderingAPIView, CustomUpdateOrderingLoanAPIView
from .markdowns import LoanMarkdownsCreateAPIView, LoanMarkdownsListAPIView