from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    Usuario, Cliente, Producto, Inventario, Pedido,
    ProductoPedido, EstadoPedido, MetodoPago
)

# 1. GESTIÓN DE USUARIOS
@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'telefono', 'dni', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'dni', 'telefono')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('dni', 'telefono', 'rol')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('dni', 'telefono', 'rol')
        }),
    )


# 2. GESTIÓN DE CLIENTES
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'telefono', 'direccion')
    search_fields = ('nombre', 'apellido', 'email', 'telefono', 'direccion')
    list_per_page = 20


# 3. INVENTARIO CONECTADO AL PRODUCTO (INLINE)
class InventarioInline(admin.StackedInline):
    model = Inventario
    extra = 1
    max_num = 1
    can_delete = False


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_producto', 'precio_unidad', 'stock_disponible', 'sabor', 'nivel_dulzura', 'tamano', 'cobertura', 'fruta', 'vista_previa_imagen')
    list_filter = ('nivel_dulzura', 'tamano', 'sabor')
    search_fields = ('nombre_producto', 'sabor', 'cobertura', 'fruta', 'descripcion')
    list_editable = ('precio_unidad',)
    inlines = [InventarioInline]
    list_per_page = 15

    def stock_disponible(self, obj):
        inv = obj.inventario.first()
        if not inv:
            return format_html('<span style="color: red;">Sin Inventario</span>')
        if inv.stock <= 0:
            return format_html('<span style="color: red; font-weight: bold;">AGOTADO (0)</span>')
        return format_html('<span style="color: green; font-weight: bold;">{} unidades</span>', inv.stock)
    stock_disponible.short_description = "Stock en Inventario"

    def vista_previa_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />', obj.imagen.url)
        return "Sin imagen"
    vista_previa_imagen.short_description = "Vista Previa"


# 4. GESTIÓN DE INVENTARIO Y STOCK
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'nombre_categoria', 'stock', 'estado_stock')
    list_editable = ('stock',)
    search_fields = ('producto__nombre_producto', 'nombre_categoria')
    list_filter = ('nombre_categoria',)

    def estado_stock(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="color: red; font-weight: bold;">AGOTADO (0)</span>')
        elif obj.stock <= 5:
            return format_html('<span style="color: orange; font-weight: bold;">CRÍTICO ({})</span>', obj.stock)
        return format_html('<span style="color: green; font-weight: bold;">DISPONIBLE ({})</span>', obj.stock)
    estado_stock.short_description = "Nivel de Stock"


# 5. DETALLES EN LÍNEA PARA PEDIDOS
class ProductoPedidoInline(admin.TabularInline):
    model = ProductoPedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'subtotal')
    can_delete = False


# 6. GESTIÓN DE PEDIDOS
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'usuario', 'estado', 'metodo_entrega', 'metodo_pago', 'total_formateado', 'tiempo_estimado', 'fecha_pedido')
    list_filter = ('estado', 'metodo_entrega', 'metodo_pago', 'fecha_pedido')
    list_editable = ('estado',)
    search_fields = ('id', 'cliente__nombre', 'cliente__email', 'usuario__username')
    inlines = [ProductoPedidoInline]
    list_per_page = 20

    def total_formateado(self, obj):
        return f"S/ {obj.total:.2f}"
    total_formateado.short_description = "Total"


# 7. REGISTRO DE HISTORIAL DE ESTADOS Y MÉTODOS DE PAGO
@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'estado', 'fecha_cambio')
    list_filter = ('estado', 'fecha_cambio')


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'metodo', 'monto', 'fecha_pago')
    list_filter = ('metodo', 'fecha_pago')
