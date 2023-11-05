from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from app.authentication.serializers import ListAdminUsersSerializer
from app.authentication.models import User

class ListAdminUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListAdminUsersSerializer
    pagination_class = None

    def get_queryset(self):
        # return superuser or staff users
        return User.objects.filter(is_superuser=True) | User.objects.filter(is_staff=True)
