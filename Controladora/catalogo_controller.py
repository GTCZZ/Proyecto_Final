import traceback
from django.shortcuts import render, redirect
from django.http import JsonResponse
from Negocio.catalogo_service import CatalogoService
from Negocio.carrito_service import CarritoService
from Negocio.chatbot_service import ChatbotService
from Negocio.pedido_service import PedidoService

class CatalogoController:
    @staticmethod
    def tienda_controller(request):
        productos = CatalogoService.obtener_todos_los_productos()
        return render(request, 'tienda.html', {'productos': productos})

    @staticmethod
    def agregar_carrito_controller(request, producto_id):
        CarritoService.agregar_producto(request.session, producto_id)
        return redirect('tienda')

    @staticmethod
    def repetir_pedido_controller(request, pedido_id):
        """
        Capa Controladora: Carga los productos de un pedido anterior en el carrito y redirige.
        """
        CarritoService.repetir_pedido_en_carrito(request.session, pedido_id)
        return redirect('ver_carrito')

    @staticmethod
    def ver_carrito_controller(request):
        datos_carrito = CarritoService.obtener_carrito_detallado(request.session)
        productos_en_carrito = datos_carrito['productos_en_carrito']
        total = datos_carrito['total']
        hay_error_stock = datos_carrito['hay_error_stock']
        error_mensaje = None

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('login')

            metodo_entrega = request.POST.get('metodo_entrega', 'DELIVERY')
            metodo_pago = request.POST.get('metodo_pago', '')

            if not metodo_pago:
                error_mensaje = "Por favor selecciona un método de pago antes de continuar con la compra."
            elif hay_error_stock:
                error_mensaje = "Uno o más productos superan la cantidad disponible en stock. Ajusta las cantidades."
            else:
                pedido = PedidoService.crear_pedido_desde_carrito(
                    usuario=request.user,
                    productos_en_carrito=productos_en_carrito,
                    total=total,
                    metodo_entrega=metodo_entrega,
                    metodo_pago=metodo_pago
                )

                CarritoService.vaciar_carrito(request.session)
                return redirect('confirmacion_pedido', pedido_id=pedido.id)

        contexto = {
            'productos_en_carrito': productos_en_carrito,
            'total': total,
            'hay_error_stock': hay_error_stock,
            'error_mensaje': error_mensaje
        }
        return render(request, 'carrito.html', contexto)

    @staticmethod
    def confirmacion_pedido_controller(request, pedido_id):
        pedido = PedidoService.obtener_pedido_por_id(pedido_id)
        if not pedido:
            return redirect('tienda')
        return render(request, 'confirmacion_pedido.html', {'pedido': pedido})

    @staticmethod
    def api_mis_pedidos_controller(request):
        data = PedidoService.obtener_datos_live_usuario(request.user)
        return JsonResponse(data)

    @staticmethod
    def api_chat_controller(request):
        try:
            mensaje_usuario = request.GET.get('mensaje', '')
            respuesta_bot = ChatbotService.consultar_chatbot_logico(mensaje_usuario)
            return JsonResponse({'respuesta': respuesta_bot})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'respuesta': f"⚠️ Error en el servidor lógico: {str(e)}"})

    @staticmethod
    def detalle_producto_controller(request, producto_id):
        producto, productos_relacionados = CatalogoService.obtener_detalle_producto(producto_id)
        contexto = {
            'producto': producto,
            'productos_relacionados': productos_relacionados
        }
        return render(request, 'detalle_producto.html', contexto)

    @staticmethod
    def eliminar_del_carrito_controller(request, producto_id):
        if request.method == 'POST':
            CarritoService.eliminar_producto(request.session, producto_id)
        return redirect('ver_carrito')

    @staticmethod
    def categorias_controller(request):
        query = request.GET.get('q', '')
        filtro_dulzura = request.GET.get('dulzura', '')
        filtro_tamano = request.GET.get('tamano', '')

        contexto = CatalogoService.filtrar_productos_funcional(query, filtro_dulzura, filtro_tamano)
        return render(request, 'categorias.html', contexto)
