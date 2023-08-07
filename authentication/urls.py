from django.urls import path
from authentication.views import LoginView, LogoutView, FetchUserView, CustomTokenRefreshView, ChangePasswordView,ResetEmployeePassword, DeactivateOrActivateEmployee

app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('fetchuser', FetchUserView.as_view(), name='fetchuser'),
    path('refresh_token', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('deactivate_or_activate_employee', DeactivateOrActivateEmployee.as_view(), name='deactivate_or_activate_employee'),
    path('reset_employee_password', ResetEmployeePassword.as_view(), name='reset_employee_password'),
]