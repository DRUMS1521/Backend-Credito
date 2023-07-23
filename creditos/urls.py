from django.urls import path
from creditos.views.basics import ListaCreditosView, DetalleCreditoView, CreditoCreateView

urlpatterns = [
    path('creditos/', ListaCreditosView.as_view(), name='lista_creditos'),
    path('creditos/<int:pk>/', DetalleCreditoView.as_view(), name='detalle_credito'),
    path('creditos-create/', CreditoCreateView.as_view(), name='create_creditos'),
]
