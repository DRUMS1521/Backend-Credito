from django.urls import path
from authentication.views import LoginView, LogoutView, FetchUserView, CustomTokenRefreshView, ChangePasswordView

app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('fetchuser', FetchUserView.as_view(), name='fetchuser'),
    path('refresh_token', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
]