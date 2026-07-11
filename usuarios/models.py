from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    # AbstractUser ya incluye: username, password, first_name, last_name, email
    
    dni = models.CharField(max_length=8, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('CAJERO', 'Cajero'),
        ('REPARTIDOR', 'Repartidor'),
        ('CLIENTE', 'Cliente'),
    )
    rol = models.CharField(max_length=15, choices=ROLES, default='CLIENTE')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"