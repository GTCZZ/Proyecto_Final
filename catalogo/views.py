from urllib import request
from pedidos.models import Pedido, ProductoPedido, Cliente
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 # Añade esto en tus importaciones de arriba
from .models import Producto
from functools import reduce
from django.http import JsonResponse
from .chatbot_logico import consultar_chatbot
import traceback
from django.http import JsonResponse
from .chatbot_logico import consultar_chatbot
# Create your views here.

def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo/tienda.html', {'productos': productos})

def agregar_carrito(request, producto_id):

    carrito = request.session.get('carrito', {})

    # Las sesiones de Django guardan datos en formato JSON, así que el ID debe ser texto
    id_str = str(producto_id)

    # Si el producto ya está en el carrito, aumentamos la cantidad
    if id_str in carrito:
        carrito[id_str] += 1
    else:
        # Si no está, lo agregamos con cantidad 1
        carrito[id_str] = 1

    # Guardamos el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    # Redirigimos de vuelta a la página de la tienda
    return redirect('catalogo:tienda')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})

    # --- PARADIGMA FUNCIONAL APLICADO ---
    # 1. Función pura que transforma un elemento del carrito en un diccionario con sus datos
    def crear_item(item_tupla):
        producto_id, cantidad = item_tupla
        prod = Producto.objects.get(id=producto_id)
        return {
            'producto': prod,
            'cantidad': cantidad,
            'subtotal': prod.precio_unidad * cantidad
        }

    # 2. Uso de MAP: Transformamos el carrito crudo en una lista de diccionarios completos
    # Sin usar bucles 'for' mutables.
    productos_en_carrito = list(map(crear_item, carrito.items()))

    # 3. Uso de REDUCE y LAMBDA: Calculamos el total sumando los subtotales 
    # de forma inmutable. (Acumulador inicia en 0)
    total = reduce(lambda acumulador, item: acumulador + item['subtotal'], productos_en_carrito, 0)
    # ------------------------------------

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('usuarios:login')

        cliente_real, creado = Cliente.objects.get_or_create(
            email=request.user.email,
            defaults={
                'nombre': request.user.first_name or request.user.username,
                'apellido': request.user.last_name or '',
                'telefono': request.user.telefono if hasattr(request.user, 'telefono') else '000000000',
                'direccion': 'Dirección no registrada'
            }
        )
        
        nuevo_pedido = Pedido.objects.create(
            cliente=cliente_real,
            usuario=request.user, 
            total=total,
            estado='PENDIENTE'
        )

        for item in productos_en_carrito:
            ProductoPedido.objects.create(
                pedido=nuevo_pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )

        request.session['carrito'] = {}
        return redirect('catalogo:tienda')

    contexto = {
        'productos_en_carrito': productos_en_carrito,
        'total': total
    }
    return render(request, 'catalogo/carrito.html', contexto)

# ... (tus otras vistas se quedan igual) ...

def api_chat(request):
    try:
        # 1. Recibimos el mensaje
        mensaje_usuario = request.GET.get('mensaje', '')
        
        # 2. Intentamos usar el motor lógico
        respuesta_bot = consultar_chatbot(mensaje_usuario)
        
        # 3. Si todo sale bien, devolvemos la respuesta normal
        return JsonResponse({'respuesta': respuesta_bot})
        
    except Exception as e:
        # SI PYTHON FALLA, atrapamos el error y lo imprimimos en la terminal negra
        print("====== ERROR EN EL CHATBOT ======")
        traceback.print_exc()
        print("=================================")
        
        # Y le enviamos el error al frontend en formato JSON para que no se rompa el JS
        return JsonResponse({'respuesta': f"⚠️ Error en el servidor lógico: {str(e)}"})
    
  
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    # Buscamos 5 productos aleatorios (excluyendo el que ya estamos viendo) para el carrusel
    productos_relacionados = Producto.objects.exclude(id=producto_id).order_by('?')[:5]
    
    contexto = {
        'producto': producto,
        'productos_relacionados': productos_relacionados
    }
    return render(request, 'catalogo/detalle_producto.html', contexto)

def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        prod_id = str(producto_id)
        
        # Si el producto está en el carrito, lo borramos de la memoria
        if prod_id in carrito:
            del carrito[prod_id]
            request.session['carrito'] = carrito
            
    return redirect('catalogo:ver_carrito')

def categorias(request):
    # 1. Obtenemos TODOS los productos y los convertimos en una lista estándar de Python
    # para poder aplicar el paradigma funcional en memoria.
    productos = list(Producto.objects.all())
    
    # Capturamos lo que el usuario envía por la URL (ej. ?q=chocolate&dulzura=Alto)
    query = request.GET.get('q', '').lower()
    filtro_dulzura = request.GET.get('dulzura', '')
    filtro_tamano = request.GET.get('tamano', '')

    # === APLICANDO PROGRAMACIÓN FUNCIONAL ===
    
    # Filtrar por Nombre
    if query:
        productos = list(filter(lambda p: query in p.nombre_producto.lower(), productos))
        
    # Filtrar por Nivel de Dulzura
    if filtro_dulzura:
        productos = list(filter(lambda p: p.nivel_dulzura == filtro_dulzura, productos))
        
    # Filtrar por Tamaño
    if filtro_tamano:
        productos = list(filter(lambda p: p.tamano == filtro_tamano, productos))

    # Usamos map() para extraer solo las columnas que nos interesan y set() para borrar duplicados.
    # Así armamos los selectores del HTML de forma dinámica.
    todos_los_productos = Producto.objects.all()
    opciones_dulzura = set(filter(None, map(lambda p: p.nivel_dulzura, todos_los_productos)))
    opciones_tamano = set(filter(None, map(lambda p: p.tamano, todos_los_productos)))

    contexto = {
        'productos': productos,
        'opciones_dulzura': opciones_dulzura,
        'opciones_tamano': opciones_tamano,
    }
    return render(request, 'catalogo/categorias.html', contexto)