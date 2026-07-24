from django.shortcuts import get_object_or_404
from .models import Producto

class CatalogoService:
    @staticmethod
    def obtener_todos_los_productos():
        return Producto.objects.all()

    @staticmethod
    def obtener_detalle_producto(producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        productos_relacionados = Producto.objects.exclude(id=producto_id).order_by('?')[:5]
        return producto, productos_relacionados

    @staticmethod
    def filtrar_productos_funcional(query, filtro_dulzura, filtro_tamano):
        """
        PARADIGMA FUNCIONAL: Filtra productos usando 'filter' y 'map'
        """
        productos = list(Producto.objects.all())

        if query:
            productos = list(filter(lambda p: query.lower() in p.nombre_producto.lower(), productos))

        if filtro_dulzura:
            productos = list(filter(lambda p: p.nivel_dulzura == filtro_dulzura, productos))

        if filtro_tamano:
            productos = list(filter(lambda p: p.tamano == filtro_tamano, productos))

        todos_los_productos = Producto.objects.all()
        opciones_dulzura = set(filter(None, map(lambda p: p.nivel_dulzura, todos_los_productos)))
        opciones_tamano = set(filter(None, map(lambda p: p.tamano, todos_los_productos)))

        return {
            'productos': productos,
            'opciones_dulzura': opciones_dulzura,
            'opciones_tamano': opciones_tamano
        }
