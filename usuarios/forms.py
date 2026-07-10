from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroClienteForm(UserCreationForm):
    # Agregamos este campo manualmente porque no existe en la tabla "Usuario"
    direccion = forms.CharField(
        max_length=255, 
        required=True, 
        label='Dirección de entrega',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Av. Ejército 101, Arequipa'})
    )

    class Meta:
        model = Usuario
        # Solo listamos los campos que pertenecen a la tabla Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'telefono', 'direccion']