from .usuario_controller import UsuarioController
from .catalogo_controller import CatalogoController

# Vistas de Usuarios
def registro_cliente(request):
    return UsuarioController.registro_cliente_controller(request)

def login_usuario(request):
    return UsuarioController.login_usuario_controller(request)

def logout_usuario(request):
    return UsuarioController.logout_usuario_controller(request)

def api_configuracion(request):
    return UsuarioController.api_configuracion_controller(request)

# Vistas de Catálogo, Carrito, Confirmación, Repetir Pedido y APIs
def tienda(request):
    return CatalogoController.tienda_controller(request)

def agregar_carrito(request, producto_id):
    return CatalogoController.agregar_carrito_controller(request, producto_id)

def repetir_pedido(request, pedido_id):
    return CatalogoController.repetir_pedido_controller(request, pedido_id)

def ver_carrito(request):
    return CatalogoController.ver_carrito_controller(request)

def confirmacion_pedido(request, pedido_id):
    return CatalogoController.confirmacion_pedido_controller(request, pedido_id)

def api_mis_pedidos(request):
    return CatalogoController.api_mis_pedidos_controller(request)

def api_chat(request):
    return CatalogoController.api_chat_controller(request)

def detalle_producto(request, producto_id):
    return CatalogoController.detalle_producto_controller(request, producto_id)

def eliminar_del_carrito(request, producto_id):
    return CatalogoController.eliminar_del_carrito_controller(request, producto_id)

def categorias(request):
    return CatalogoController.categorias_controller(request)
