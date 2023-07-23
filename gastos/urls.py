from django.urls import path
from gastos.views import GastosCreateView, GastosDetailView, GastosListView

urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='lista_gastos'),
    path('gastos/<int:pk>/', GastosDetailView.as_view(), name='create_gastos'),
    path('gastos-create/', GastosCreateView.as_view(), name='create_gastos'),
]
