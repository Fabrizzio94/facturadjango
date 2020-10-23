from django.urls import path
# from .views import FacturaListView, FacturaFormView
from .views import  ClienteView
urlpatterns = [
    path('', ClienteView.as_view(), name='factura'),
    #path('listproducto/', ProductListView.as_view(), name='producto')
]
