from app.loans.serializers import CreatePaymentSerializer
from app.loans.models import Payment, Loan
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class CreatePaymentAPIView(generics.CreateAPIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # get loan from kwargs
        loan = kwargs.get('loan', None)
        if loan is None:
            return Response({'detail': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        # Add loan to request data
        request.data['loan'] = loan
        serializer = CreatePaymentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Create payment
        payment = serializer.save()        
        return Response({'id': payment.id, 'created_at': payment.created_at}, status=status.HTTP_201_CREATED)

