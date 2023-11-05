from django.urls import path
from .views import *

urlpatterns = [
    path('spends', SpendListCreateAPIView.as_view(), name='spends'),
]