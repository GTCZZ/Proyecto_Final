from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Controladora import views

# Enrutamiento de la Capa Controladora
catalogo_patterns = ([
    path('', views.tienda, name='tienda'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('repetir-pedido/<int:pedido_id>/', views.repetir_pedido, name='repetir_pedido'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('api/mis-pedidos/', views.api_mis_pedidos, name='api_mis_pedidos'),
    path('api/configuracion/', views.api_configuracion, name='api_configuracion'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_carrito'),
    path('categorias/', views.categorias, name='categorias'),
], 'catalogo')

usuarios_patterns = ([
    path('registro/', views.registro_cliente, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
], 'usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas unificadas sin namespace
    path('', views.tienda, name='tienda'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('repetir-pedido/<int:pedido_id>/', views.repetir_pedido, name='repetir_pedido'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('api/mis-pedidos/', views.api_mis_pedidos, name='api_mis_pedidos'),
    path('api/configuracion/', views.api_configuracion, name='api_configuracion'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_carrito'),
    path('categorias/', views.categorias, name='categorias'),
    path('cuenta/registro/', views.registro_cliente, name='registro'),
    path('cuenta/login/', views.login_usuario, name='login'),
    path('cuenta/logout/', views.logout_usuario, name='logout'),

    # Alias con namespaces para compatibilidad completa
    path('', include(catalogo_patterns)),
    path('cuenta/', include(usuarios_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
