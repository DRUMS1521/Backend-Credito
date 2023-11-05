from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.loans.serializers.customer_loan import CustomerLoanSerializer
from app.loans.models import Loan, Payment

class CustomerLoanAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerLoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(status=status.HTTP_201_CREATED)