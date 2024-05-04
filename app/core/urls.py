from django.urls import path
from .views import uploadFileAPIView, InfoAndRulesAPIView, healthCheckAPIView, CustomConfigAPIView

urlpatterns = [
    path('upload', uploadFileAPIView.as_view(), name='upload'),
    path('info', InfoAndRulesAPIView.as_view(), name='info'),
    path('health', healthCheckAPIView.as_view(), name='health'),
    path('config', CustomConfigAPIView.as_view(), name='config'),
]