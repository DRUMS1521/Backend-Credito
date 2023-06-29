from django.urls import path
from creditos.views.basics import ListaCreditosView, DetalleCreditoView

urlpatterns = [
    path('creditos/', ListaCreditosView.as_view(), name='lista_creditos'),
    path('creditos/<int:pk>/', DetalleCreditoView.as_view(), name='detalle_credito'),
]
