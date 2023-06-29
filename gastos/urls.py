from django.urls import path
from gastos.views import *

urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='lista_gastos'),
    path('gastos-create/', GastosDetailView.as_view(), name='create_gastos'),
]
