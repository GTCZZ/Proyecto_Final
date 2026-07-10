from django.contrib import admin
from .models import Cliente, Pedido, ProductoPedido, EstadoPedido, MetodoPago
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(ProductoPedido)
admin.site.register(EstadoPedido)
admin.site.register(MetodoPago)

