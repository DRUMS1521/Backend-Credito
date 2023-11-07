from django.urls import path
from .views import uploadFileAPIView, InfoAndRulesAPIView

urlpatterns = [
    path('upload', uploadFileAPIView.as_view(), name='upload'),
    path('info', InfoAndRulesAPIView.as_view(), name='info'),
]