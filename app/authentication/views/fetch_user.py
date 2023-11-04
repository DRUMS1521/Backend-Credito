from app.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from app.authentication.serializers import FetchUserSerializer

class FetchUserApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = FetchUserSerializer

    def get_object(self):
        return self.request.user