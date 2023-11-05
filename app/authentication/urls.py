from django.urls import path
from app.authentication.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name="login"),
    path('me', FetchUserApiView.as_view(), name="fetch"),
    path('admin-users', ListAdminUsersAPIView.as_view(), name="admin-users"),
]