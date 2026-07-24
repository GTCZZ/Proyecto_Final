from functools import reduce
from .models import Producto, Inventario, ProductoPedido

class CarritoService:
    @staticmethod
    def agregar_producto(session, producto_id):
        carrito = session.get('carrito', {})
        id_str = str(producto_id)

        if id_str in carrito:
            carrito[id_str] += 1
        else:
            carrito[id_str] = 1

        session['carrito'] = carrito
        return carrito

    @staticmethod
    def eliminar_producto(session, producto_id):
        carrito = session.get('carrito', {})
        prod_id = str(producto_id)

        if prod_id in carrito:
            del carrito[prod_id]
            session['carrito'] = carrito
        return carrito

    @staticmethod
    def repetir_pedido_en_carrito(session, pedido_id):
        """
        Carga todos los productos de un pedido anterior en la sesión del carrito actual.
        """
        detalles = ProductoPedido.objects.filter(pedido_id=pedido_id)
        carrito = session.get('carrito', {})

        for d in detalles:
            id_str = str(d.producto_id)
            carrito[id_str] = carrito.get(id_str, 0) + d.cantidad

        session['carrito'] = carrito
        return carrito

    @staticmethod
    def obtener_carrito_detallado(session):
        """
        PARADIGMA FUNCIONAL: Calcula subtotales y total con 'map' y 'reduce',
        e incluye la verificación de stock por cada ítem.
        """
        carrito = session.get('carrito', {})

        def crear_item(item_tupla):
            producto_id, cantidad = item_tupla
            prod = Producto.objects.get(id=producto_id)
            inv = Inventario.objects.filter(producto=prod).first()
            stock_disponible = inv.stock if inv else 10
            return {
                'producto': prod,
                'cantidad': cantidad,
                'subtotal': prod.precio_unidad * cantidad,
                'stock_disponible': stock_disponible,
                'sin_stock': cantidad > stock_disponible
            }

        productos_en_carrito = list(map(crear_item, carrito.items()))
        total = reduce(lambda acumulador, item: acumulador + item['subtotal'], productos_en_carrito, 0)
        
        hay_error_stock = any(map(lambda item: item['sin_stock'], productos_en_carrito))

        return {
            'productos_en_carrito': productos_en_carrito,
            'total': total,
            'hay_error_stock': hay_error_stock
        }

    @staticmethod
    def vaciar_carrito(session):
        session['carrito'] = {}
