from django.db import models
from django.contrib.auth.models import AbstractUser

# --- MODELOS DE USUARIO ---
class Usuario(AbstractUser):
    dni = models.CharField(max_length=8, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('CAJERO', 'Cajero'),
        ('REPARTIDOR', 'Repartidor'),
        ('CLIENTE', 'Cliente'),
    )
    rol = models.CharField(max_length=15, choices=ROLES, default='CLIENTE')

    class Meta:
        db_table = 'usuarios_usuario'

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


# --- MODELOS DE CATÁLOGO E INVENTARIO ---
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    NIVELES_DULZURA = (('BAJO', 'Bajo'), ('MEDIO', 'Medio'), ('ALTO', 'Alto'))
    TAMANOS = (('PEQUEÑO', 'Pequeño'), ('MEDIANO', 'Mediano'), ('GRANDE', 'Grande'))

    sabor = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: Chocolate, Vainilla")
    nivel_dulzura = models.CharField(max_length=20, choices=NIVELES_DULZURA, null=True, blank=True)
    fruta = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: Fresa, Durazno")
    cobertura = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: Chantilly, Fondant")
    tamano = models.CharField(max_length=20, choices=TAMANOS, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción del postre")
    
    class Meta:
        db_table = 'catalogo_producto'

    def __str__(self):
        return self.nombre_producto


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario')
    nombre_categoria = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = 'catalogo_inventario'

    def __str__(self):
        return f"{self.producto.nombre_producto} - Stock: {self.stock}"


# --- MODELOS DE PEDIDOS Y CLIENTES ---
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255)

    class Meta:
        db_table = 'pedidos_cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Pedido(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('ENTREGADO', 'Entregado'),
        ('FALLIDO', 'Fallido'),
    )
    METODOS_ENTREGA = (
        ('DELIVERY', 'Delivery a Domicilio'),
        ('RETIRO', 'Retiro en Tienda'),
    )
    METODOS_PAGO = (
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia Bancaria / Yape'),
        ('PAYPAL', 'PayPal'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    metodo_entrega = models.CharField(max_length=20, choices=METODOS_ENTREGA, default='DELIVERY')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='TARJETA')
    tiempo_estimado = models.CharField(max_length=50, default='35 - 45 minutos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'pedidos_pedido'

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"


class ProductoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos_productopedido'

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre_producto} (Pedido #{self.pedido.id})"


class EstadoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='estados')
    estado = models.CharField(max_length=20, choices=Pedido.ESTADOS)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedidos_estadopedido'

    def __str__(self):
        return f"Pedido #{self.pedido.id} - {self.estado} ({self.fecha_cambio})"


class MetodoPago(models.Model):
    METODOS = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('PAYPAL', 'PayPal'),
    )
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='metodos_pago')
    metodo = models.CharField(max_length=20, choices=METODOS)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos_metodopago'

    def __str__(self):
        return f"Pedido #{self.pedido.id} - {self.metodo} ({self.monto})"


# --- SEÑALES DE NEGOCIO: VINCULACIÓN AUTOMÁTICA DE PRODUCTO E INVENTARIO ---
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Producto)
def crear_inventario_producto(sender, instance, created, **kwargs):
    """
    Sincroniza automáticamente la creación de un Producto con su registro de Inventario.
    """
    if created:
        Inventario.objects.get_or_create(
            producto=instance,
            defaults={'nombre_categoria': 'Pastelería Fina', 'stock': 20}
        )

