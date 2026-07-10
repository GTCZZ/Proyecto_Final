from django.db import models
from usuarios.models import Usuario
from catalogo.models import Producto

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Pedido(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('ENTREGADO', 'Entregado'),
        ('FALLIDO', 'Fallido'),
    )
    # Relaciones (Foreign Keys)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos de datos
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"

class ProductoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre_producto} (Pedido #{self.pedido.id})"

class EstadoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='estados')
    estado = models.CharField(max_length=20, choices=Pedido.ESTADOS)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"Pedido #{self.pedido.id} - {self.metodo} ({self.monto})"
        