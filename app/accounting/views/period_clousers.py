from app.accounting.models import PeriodClosures, UserGoals
from app.accounting.serializers import PeriodClosuresSerializer, NewPeriodClosureSerializer, UserGoalsSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from app.authentication.models import User

class PeriodClosuresListCreateView(generics.ListCreateAPIView):
    serializer_class = PeriodClosuresSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None
    queryset = PeriodClosures.objects.all()

class PeriodClosureCustomCreateView(generics.CreateAPIView):
    serializer_class = NewPeriodClosureSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None
    queryset = PeriodClosures.objects.all()

class PeriodClosuresRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PeriodClosuresSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None
    queryset = PeriodClosures.objects.all()

class ActualPeriodClosureRetrieveAPIView(generics.GenericAPIView):
    serializer_class = PeriodClosuresSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        # Retrieve the current period (the one that is not closed)
        try:
            queryset = PeriodClosures.get_open_period()
        except:
            queryset = PeriodClosures.objects.none()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserGoalsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserGoalsSerializer
    pagination_class = None
    queryset = UserGoals.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_object(self):
        # Check if request user is superuser
        request_user = self.request.user
        current_period = PeriodClosures.get_open_period()
        if not request_user.is_superuser:
            # If user is not superuser, return the user goals for the current period
            obj = UserGoals.objects.filter(user=request_user, period_closure=current_period).first()
            return obj
        else:
            # If user is superuser, return the user goals for the user in the URL
            user_id = self.kwargs.get('user_id', None)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = self.request.user
            obj = UserGoals.objects.filter(user=user, period_closure=current_period).first()
            return obj