from .models import Cliente

class UsuarioService:
    @staticmethod
    def registrar_cliente(form):
        """
        Guarda el usuario con rol CLIENTE y sincroniza con la entidad Cliente.
        """
        usuario = form.save(commit=False)
        usuario.rol = 'CLIENTE'
        usuario.save()

        direccion_ingresada = form.cleaned_data.get('direccion')

        Cliente.objects.create(
            nombre=usuario.first_name,
            apellido=usuario.last_name,
            email=usuario.email,
            telefono=usuario.telefono,
            direccion=direccion_ingresada
        )
        return usuario

    @staticmethod
    def obtener_usuario_autenticado(form):
        return form.get_user()

    @staticmethod
    def actualizar_perfil_usuario(usuario, datos):
        """
        Actualiza los datos personales del usuario y sincroniza con la entidad Cliente.
        """
        if not usuario.is_authenticated:
            return False, "Usuario no autenticado."

        nombre = datos.get('nombre', '').strip()
        apellido = datos.get('apellido', '').strip()
        email = datos.get('email', '').strip()
        telefono = datos.get('telefono', '').strip()
        direccion = datos.get('direccion', '').strip()

        if nombre: usuario.first_name = nombre
        if apellido: usuario.last_name = apellido
        if email: usuario.email = email
        if telefono: usuario.telefono = telefono
        usuario.save()

        # Sincronizar entidad Cliente
        cliente, creado = Cliente.objects.get_or_create(
            email=usuario.email,
            defaults={
                'nombre': usuario.first_name,
                'apellido': usuario.last_name,
                'telefono': usuario.telefono or '000000000',
                'direccion': direccion or 'Dirección no registrada'
            }
        )
        if not creado:
            if nombre: cliente.nombre = nombre
            if apellido: cliente.apellido = apellido
            if telefono: cliente.telefono = telefono
            if direccion: cliente.direccion = direccion
            cliente.save()

        return True, "Datos personales actualizados correctamente."

    @staticmethod
    def cambiar_password_usuario(usuario, pass_actual, pass_nuevo):
        """
        Verifica la contraseña actual y actualiza a la nueva clave.
        """
        if not usuario.is_authenticated:
            return False, "Usuario no autenticado."

        if not usuario.check_password(pass_actual):
            return False, "La contraseña actual ingresada es incorrecta."

        if len(pass_nuevo) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres."

        usuario.set_password(pass_nuevo)
        usuario.save()
        return True, "Contraseña actualizada exitosamente."
