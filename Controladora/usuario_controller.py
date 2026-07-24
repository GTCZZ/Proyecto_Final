from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from Presentacion.forms import RegistroClienteForm
from Negocio.usuario_service import UsuarioService
from Negocio.models import Cliente

class UsuarioController:
    @staticmethod
    def registro_cliente_controller(request):
        if request.method == 'POST':
            form = RegistroClienteForm(request.POST)
            if form.is_valid():
                usuario = UsuarioService.registrar_cliente(form)
                login(request, usuario)
                return redirect('tienda')
        else:
            form = RegistroClienteForm()
        return render(request, 'registro.html', {'form': form})

    @staticmethod
    def login_usuario_controller(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                usuario = UsuarioService.obtener_usuario_autenticado(form)
                login(request, usuario)
                return redirect('tienda')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    @staticmethod
    def logout_usuario_controller(request):
        logout(request)
        return redirect('tienda')

    @staticmethod
    def api_configuracion_controller(request):
        """
        Capa Controladora: Endpoint AJAX para actualizar perfil, contraseña
        o guardar método de pago predeterminado desde la pestaña ⚙️ Configuración.
        """
        if not request.user.is_authenticated:
            return JsonResponse({'ok': False, 'mensaje': 'Debes iniciar sesión para realizar cambios.'})

        if request.method == 'POST':
            accion = request.POST.get('accion', '')

            if accion == 'perfil':
                ok, msg = UsuarioService.actualizar_perfil_usuario(request.user, request.POST)
                return JsonResponse({'ok': ok, 'mensaje': msg})

            elif accion == 'password':
                pass_actual = request.POST.get('pass_actual', '')
                pass_nuevo = request.POST.get('pass_nuevo', '')
                ok, msg = UsuarioService.cambiar_password_usuario(request.user, pass_actual, pass_nuevo)
                if ok:
                    update_session_auth_hash(request, request.user)
                return JsonResponse({'ok': ok, 'mensaje': msg})

            elif accion == 'metodo_pago':
                metodo = request.POST.get('metodo_pago_pref', '')
                num_tarjeta = request.POST.get('num_tarjeta', '')
                paypal_email = request.POST.get('paypal_email', '')

                request.session['metodo_pago_guardado'] = {
                    'metodo': metodo,
                    'num_tarjeta': num_tarjeta[-4:] if num_tarjeta else '',
                    'paypal_email': paypal_email
                }
                return JsonResponse({'ok': True, 'mensaje': 'Método de pago predeterminado guardado exitosamente.'})

        # GET: Retornar datos actuales del usuario
        cliente = Cliente.objects.filter(email=request.user.email).first()
        metodo_guardado = request.session.get('metodo_pago_guardado', {})

        return JsonResponse({
            'ok': True,
            'nombre': request.user.first_name,
            'apellido': request.user.last_name,
            'email': request.user.email,
            'telefono': request.user.telefono or '',
            'direccion': cliente.direccion if cliente else 'Dirección no registrada',
            'metodo_guardado': metodo_guardado
        })
