from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from usuarios.models import RegistroSesion
from usuarios.models import Usuario

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        # Intenta autenticar al usuario
        user = authenticate(request, username=username, password=password)

        # Verifica si la autenticación fue exitosa
        if user is not None:
            # Si el usuario ya tiene una sesión activa en otro dispositivo
            if user.session_active:
                return render(request, 'login.html', {'error_message': 'Ya has iniciado sesión en otro dispositivo.'})

            # Inicia sesión para el usuario autenticado
            login(request, user)
            
            # Guardar el ID del usuario en la sesión
            request.session['user_id'] = user.id

            # Actualiza el campo session_active a True
            user.session_active = True
            user.save()

            # Registra el inicio de sesión en la tabla RegistroSesion
            RegistroSesion.objects.create(usuario=user, fecha_inicio=timezone.now())

            return redirect('dashboard')
        else:
            # Si la autenticación falla, muestra un mensaje de error
            return render(request, 'login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos.'})
        

def cerrar_sesion(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener el ID del usuario de la sesión
        user_id = request.session.get('user_id')

        # Si se obtiene el ID del usuario, obtener y actualizar el registro de sesión correspondiente
        if user_id:
            try:
                usuario = Usuario.objects.get(id=user_id)
                usuario.session_active = False
                ultimo_registro = RegistroSesion.objects.filter(usuario_id=user_id).latest('fecha_inicio')
                # Actualizar la fecha de cierre del último registro obtenido
                ultimo_registro.fecha_cierre = timezone.now()
                ultimo_registro.save()

                usuario.save()
            except RegistroSesion.DoesNotExist:
                pass
        
        logout(request)
        
        return redirect('iniciar_sesion')
    else:
            return redirect('iniciar_sesion')
