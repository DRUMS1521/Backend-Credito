from django.urls import path
from creditos.views.basics import ListaCreditosView, DetalleCreditoView
from creditos.views import ListPaymentsView, UpdatePaymentsView

urlpatterns = [
    path('creditos', ListaCreditosView.as_view(), name='lista_creditos'),
    path('creditos/<int:pk>/', DetalleCreditoView.as_view(), name='detalle_credito'),
    #payments
    path('payments', ListPaymentsView.as_view(), name='lista_payments'),
    path('payments/<int:pk>', UpdatePaymentsView.as_view(), name='detalle_payments'),
]
