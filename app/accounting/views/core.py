from app.accounting.models import Wallet, WalletMovement
from app.accounting.serializers import SpendSerializer, DepositSerializer, WalletSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

class WalletCheckerAPIView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        # Get request user wallet
        wallet = Wallet.objects.get(user=self.request.user)
        return wallet

class SpendListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SpendSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        user = self.request.user
        # Get date from query params
        date = self.request.query_params.get('date', None)
        # Get user from query params if user is staff
        if user.is_staff | user.is_superuser:
            requested_user = self.request.query_params.get('user', None)
            if requested_user is not None and requested_user != '' and requested_user != '0' and requested_user != 0 and requested_user != 'all':
                usr = requested_user
            else:
                usr = user.id
        else:
            usr = user.id
        # Get request user wallet
        wallet = Wallet.objects.get(user__id=usr)
        if date is not None:
            return WalletMovement.objects.filter(wallet=wallet, created_at__date=date, type='exit').order_by('-id')
        else:
            return WalletMovement.objects.filter(wallet=wallet, type='exit').order_by('-id')

    def post(self, request, *args, **kwargs):
        serializer = SpendSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Create movement
            movement = serializer.save()
            return Response({'id': movement.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DepositListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        # Get request user wallet
        wallet = Wallet.objects.get(user=self.request.user)
        # Get date from query params
        date = self.request.query_params.get('date', None)
        if date is not None:
            return WalletMovement.objects.filter(wallet=wallet, created_at__date=date, type='entry')
        else:
            return WalletMovement.objects.filter(wallet=wallet, type='entry')
    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Create movement
            movement = serializer.save()
            return Response({'id': movement.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)