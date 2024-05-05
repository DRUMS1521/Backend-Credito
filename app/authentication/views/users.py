from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.authentication.serializers import ListAdminUsersSerializer, UsersSerializer
from app.authentication.models import User
from rest_framework.response import Response
from rest_framework import status

class ListAdminUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListAdminUsersSerializer
    pagination_class = None

    def get_queryset(self):
        # return superuser or staff users
        return User.objects.filter(is_superuser=True) | User.objects.filter(is_staff=True)

class ListCreateUsersAPIView(ListCreateAPIView):
    serializer_class = UsersSerializer
    pagination_class = None
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

class UpdateUsersAPIView(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UsersSerializer
    pagination_class = None
    queryset = User.objects.all()

class UpdateUserPasswordAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)
        if current_password is not None and new_password is not None:
            if current_password != '' and new_password != '':
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Current password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Current password or new password is empty'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Current password or new password is empty'}, status=status.HTTP_400_BAD_REQUEST)