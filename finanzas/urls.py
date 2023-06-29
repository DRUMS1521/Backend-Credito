from django.urls import path
from finanzas.views import *
urlpatterns = [
    path('finanzas/', FinanzasListView.as_view(), name='lista_finanzas'),
    path('finanzas/<int:pk>/', FinanzasDetailView.as_view(), name='detalle_finanzas'),
]
