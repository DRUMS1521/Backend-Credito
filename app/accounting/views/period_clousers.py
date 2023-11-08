from app.accounting.models import PeriodClosures
from app.accounting.serializers import PeriodClosuresSerializer, NewPeriodClosureSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

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
            queryset = PeriodClosures.objects.filter(closed=False).first()
        except:
            queryset = PeriodClosures.objects.none()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)