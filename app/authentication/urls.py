from django.urls import path
from app.authentication.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name="login"),
    path('me', FetchUserApiView.as_view(), name="fetch"),
    path('admin-users', ListAdminUsersAPIView.as_view(), name="admin-users"),
    path('users', ListCreateUsersAPIView.as_view(), name="users"),
    path('users/<int:pk>', UpdateUsersAPIView.as_view(), name="users"),
    path('users/change_password', UpdateUserPasswordAPIView.as_view(), name="users-password"),
]