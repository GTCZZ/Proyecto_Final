from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]
