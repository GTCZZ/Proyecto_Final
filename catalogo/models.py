from django.db import models

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    NIVELES_DULZURA = (('BAJO', 'Bajo'), ('MEDIO', 'Medio'), ('ALTO', 'Alto'))
    TAMANOS = (('PEQUEÑO', 'Pequeño'), ('MEDIANO', 'Mediano'), ('GRANDE', 'Grande'))

    sabor = models.CharField(max_length=50, null=True, blank=True, help_text="Ejemplo: Chocolate, Vainilla, Fresa")
    nivel_dulzura = models.CharField(max_length=20, choices=NIVELES_DULZURA, null=True, blank=True)
    fruta = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: Fresa, Durazno, Ninguna")
    cobertura = models.CharField(max_length=50, null=True, blank=True, help_text="Ej: Chantilly, Fondant, Buttercream")
    tamano = models.CharField(max_length=20, choices=TAMANOS, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción detallada del postre")
    
    def __str__(self):
        return self.nombre_producto

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario')
    nombre_categoria = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre_producto} - Stock: {self.stock}"