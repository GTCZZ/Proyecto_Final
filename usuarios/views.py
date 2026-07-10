from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroClienteForm
from pedidos.models import Cliente 

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # 1. Guardamos los datos base en la tabla Usuario
            usuario = form.save(commit=False)
            usuario.rol = 'CLIENTE'  
            usuario.save()

            # Extraemos la dirección que el usuario acaba de escribir
            direccion_ingresada = form.cleaned_data.get('direccion')

            # 2. Guardamos en la tabla Cliente usando la dirección real
            Cliente.objects.create(
                nombre=usuario.first_name,
                apellido=usuario.last_name,
                email=usuario.email,
                telefono=usuario.telefono,
                direccion=direccion_ingresada
            )

            # 3. Iniciamos sesión y lo mandamos a comprar
            login(request, usuario)  
            return redirect('catalogo:tienda')
    else:
        form = RegistroClienteForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('catalogo:tienda')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('catalogo:tienda')