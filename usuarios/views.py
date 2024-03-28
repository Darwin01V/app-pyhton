from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Rol, Persona
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUploadForm
from .utils import process_excel_file

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre'].lower().capitalize()
            apellido = request.POST['apellido'].lower().capitalize()
            identificacion = request.POST['identificacion'].lower()
            fecha_nacimiento = request.POST['fecha_nacimiento']
            correo = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            rol_nombre = request.POST['rol']
            
            if Usuario.objects.filter(username=username).exists():
                raise ValueError('El nombre de usuario ya existe.')
            
            # Validar el nombre de usuario
            if not (username.isalnum() and any(c.isdigit() for c in username) and any(c.isupper() for c in username) and len(username) >= 8 and len(username) <= 20):
                raise ValueError('El nombre de usuario no cumple con los requisitos.')
            
            # Validar la contraseña
            if not (len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password) and not any(c.isspace() for c in password)):
                raise ValueError('La contraseña no cumple con los requisitos.')
            
            # Validar la identificación
            if not (len(identificacion) == 10 and identificacion.isdigit() and not any(identificacion[i] == identificacion[i+1] == identificacion[i+2] == identificacion[i+3] for i in range(len(identificacion)-3))):
                raise ValueError('La identificación no cumple con los requisitos.')
            
            # Crear la persona
            persona = Persona.objects.create(
                nombre=nombre,
                apellido=apellido,
                identificacion=identificacion,
                fecha_nacimiento=fecha_nacimiento
            )
            
            # Crear o obtener el rol
            rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)
            
            # Crear el usuario
            usuario = Usuario.objects.create_user(
                username=username,
                email=correo,
                password=password,
                persona=persona
            )
            
            # Guardar el usuario
            usuario.save()
            
            # Asignar el rol al usuario a través de la tabla intermedia
            rol.usuarios.add(usuario)
            
            return redirect('listar_usuarios')
        
        except Exception as e:
            error_message = str(e)
            return render(request, 'crear.html', {'error_message': error_message})
    
    else:
        return render(request, 'crear.html')

@login_required
def listar_usuarios(request):
    # Obtener todos los usuarios
    usuarios = Usuario.objects.all().order_by('id')

    # Crear una lista para almacenar los datos de usuario extendidos
    usuarios_extendidos = []

    # Iterar sobre cada usuario y obtener sus datos extendidos
    for usuario in usuarios:
        # Obtener los datos de la persona asociada al usuario
        persona = usuario.persona

        # Crear un diccionario con los datos del usuario extendido
        usuario_extendido = {
            'id': usuario.id,
            'username': usuario.username,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'email': usuario.email,
            'identificacion': persona.identificacion,
            'fecha_nacimiento': persona.fecha_nacimiento,
            'estado': usuario.status,
            'sesion': usuario.session_active
        }

        # Agregar el diccionario a la lista de usuarios extendidos
        usuarios_extendidos.append(usuario_extendido)

    # Pasar la lista de usuarios extendidos al template
    return render(request, 'listar.html', {'usuarios': usuarios_extendidos})

@login_required
def editar_usuario(request, id):
    if request.method == 'POST':
        try:
            # Obtener el usuario a editar
            usuario = Usuario.objects.get(id=id)
            # Actualizar los campos del usuario
            usuario.persona.nombre = request.POST['nombre'].lower().capitalize()
            usuario.persona.apellido = request.POST['apellido'].lower().capitalize()
            usuario.persona.identificacion = request.POST['identificacion'].lower()
            usuario.persona.fecha_nacimiento = request.POST['fecha_nacimiento']
            
            usuario.email = request.POST['email']
            usuario.username = request.POST['username']
            password = request.POST['password'] # Recuerda cambiar esto por la forma adecuada de actualizar la contraseña
            usuario.set_password(password)
            usuario.status = request.POST['status']
            
            usuario.persona.save()
            usuario.save()

            return redirect('listar_usuarios')

        except Usuario.DoesNotExist:
            # Manejar el caso en que el usuario no existe
            return render(request, 'editar.html', {'error_message': 'El usuario no existe.' })
        except Exception as e:
            # Manejar cualquier otro error
            return render(request, 'editar.html', {'error_message': str(e)})
    else:
        # Si el método HTTP es GET, mostrar el formulario de edición
        try:
            # Obtener el usuario a editar
            usuario = Usuario.objects.get(id=id)
            return render(request, 'editar.html', {'usuario': usuario})
        except Usuario.DoesNotExist:
            # Manejar el caso en que el usuario no existe
            return render(request, 'editar.html', {'error_message': 'El usuario no existe.'})

@login_required
def borrar_usuarios(request, id):
    try:
        # Obtener el usuario a borrar
        usuario = Usuario.objects.get(id=id)
        
        # Obtener la persona y el rol asociados al usuario
        persona = usuario.persona
        
        # Borrar el usuario, la persona y el rol
        usuario.delete()
        persona.delete()
        
        return redirect('listar_usuarios')  # Redirigir a la lista de usuarios u otra vista
    except Usuario.DoesNotExist:
        return HttpResponse("El usuario no existe")
    except Exception as e:
        # Manejar otras excepciones
        return HttpResponse(f"Error: {e}")

@login_required
def upload_users(request):
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if uploaded_file.name.endswith('.xlsx'):
                users_created = process_excel_file(uploaded_file)
                messages.success(request, f"{users_created} usuarios creados exitosamente.")
            else:
                messages.error(request, "Formato de archivo no compatible. Por favor, suba un archivo .xlsx.")
            #return redirect('listar_usuarios')
    else:
        form = UserUploadForm()
    return render(request, 'upload_users.html', {'form': form})
