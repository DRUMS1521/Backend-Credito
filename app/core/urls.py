from django.urls import path
from .views import uploadFileAPIView

urlpatterns = [
    path('upload', uploadFileAPIView.as_view(), name='upload'),
]