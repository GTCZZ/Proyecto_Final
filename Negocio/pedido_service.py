from .models import Pedido, ProductoPedido, Cliente, Inventario, MetodoPago

class PedidoService:
    @staticmethod
    def crear_pedido_desde_carrito(usuario, productos_en_carrito, total, metodo_entrega='DELIVERY', metodo_pago='TARJETA'):
        """
        Procesa la transacción del pedido, descuenta stock de Inventario,
        asigna tiempo estimado y registra la forma de pago.
        """
        if not productos_en_carrito:
            return None

        # 1. Descuento de stock en Inventario
        for item in productos_en_carrito:
            prod = item['producto']
            inv = Inventario.objects.filter(producto=prod).first()
            if inv:
                inv.stock = max(0, inv.stock - item['cantidad'])
                inv.save()

        # 2. Asignación del cliente
        cliente_real, creado = Cliente.objects.get_or_create(
            email=usuario.email,
            defaults={
                'nombre': usuario.first_name or usuario.username,
                'apellido': usuario.last_name or '',
                'telefono': usuario.telefono if hasattr(usuario, 'telefono') else '000000000',
                'direccion': 'Dirección no registrada'
            }
        )

        # 3. Cálculo de tiempo estimado según método de entrega
        if metodo_entrega == 'RETIRO':
            tiempo_estimado = '15 - 25 minutos (Retiro en Tienda)'
        else:
            tiempo_estimado = '35 - 45 minutos (Delivery a Domicilio)'

        # 4. Creación del Pedido
        nuevo_pedido = Pedido.objects.create(
            cliente=cliente_real,
            usuario=usuario,
            total=total,
            estado='PENDIENTE',
            metodo_entrega=metodo_entrega,
            metodo_pago=metodo_pago,
            tiempo_estimado=tiempo_estimado
        )

        # 5. Registro de detalles e historial de pago
        for item in productos_en_carrito:
            ProductoPedido.objects.create(
                pedido=nuevo_pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )

        MetodoPago.objects.create(
            pedido=nuevo_pedido,
            metodo=metodo_pago,
            monto=total
        )

        return nuevo_pedido

    @staticmethod
    def obtener_pedido_por_id(pedido_id):
        return Pedido.objects.filter(id=pedido_id).first()

    @staticmethod
    def obtener_datos_live_usuario(usuario):
        """
        Retorna los pedidos del usuario y notificaciones para el panel hamburguesa.
        """
        if not usuario.is_authenticated:
            return {'pedidos': [], 'notificaciones': []}

        pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha_pedido')
        
        lista_pedidos = []
        lista_notificaciones = []

        for p in pedidos:
            detalles = ProductoPedido.objects.filter(pedido=p)
            items_str = ", ".join([f"{d.cantidad}x {d.producto.nombre_producto}" for d in detalles])

            estado_label = p.get_estado_display()
            entrega_label = p.get_metodo_entrega_display()
            pago_label = p.get_metodo_pago_display()

            lista_pedidos.append({
                'id': p.id,
                'fecha': p.fecha_pedido.strftime('%d/%m/%Y %H:%M'),
                'estado': p.estado,
                'estado_display': estado_label,
                'total': float(p.total),
                'metodo_entrega': entrega_label,
                'metodo_pago': pago_label,
                'tiempo_estimado': p.tiempo_estimado,
                'items_resumen': items_str,
                'detalles': [{
                    'producto': d.producto.nombre_producto,
                    'cantidad': d.cantidad,
                    'subtotal': float(d.subtotal)
                } for d in detalles]
            })

            # Generar notificaciones por pedido
            lista_notificaciones.append({
                'id': f"notif_{p.id}_{p.estado}",
                'titulo': f"Pedido #{p.id} - {estado_label}",
                'mensaje': f"Tu pedido con {items_str} se encuentra en estado '{estado_label}'. Tiempo estimado: {p.tiempo_estimado}.",
                'fecha': p.fecha_pedido.strftime('%H:%M')
            })

        return {
            'pedidos': lista_pedidos,
            'notificaciones': lista_notificaciones
        }
