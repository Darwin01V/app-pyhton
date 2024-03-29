from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import xml.etree.ElementTree as ET
from django.utils import timezone
from usuarios.models import RegistroSesion, Sesiones , Usuario
from django.db.models import Count
from django.db.models.functions import TruncMonth

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        request.session['user_id'] = user.id

        if user is not None:
            if user.session_active:
                return render(request, 'cerrar_session_op.html')

            login(request, user)
            
            user.session_active = True
            user.save()

            RegistroSesion.objects.create(usuario=user, fecha_inicio=timezone.now())

            crear_xml_sesion(user, request)

            return redirect('dashboard')
        else:
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
                ultimo_registro.fecha_cierre = timezone.now()
                ultimo_registro.save()
                
                actualizar_xml_cierre(usuario)

                usuario.save()
            except RegistroSesion.DoesNotExist:
                pass
        
        logout(request)
        
        return redirect('iniciar_sesion')
    else:
            return redirect('iniciar_sesion')

def crear_xml_sesion(usuario, request):
    root = ET.Element('session')

    timein = ET.SubElement(root, 'timein')
    timein.text = timezone.localtime(timezone.now()).strftime('%H:%M:%S') 

    datein = ET.SubElement(root, 'datein')
    datein.text = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')

    ip_address = ET.SubElement(root, 'ip_address')
    ip_add = obtener_direccion_ip_del_usuario(request)
    ip_address.text = ip_add

    xml_string = ET.tostring(root, encoding='utf-8')
    sesion = Sesiones.objects.create(userID_id=usuario.id, xml=xml_string.decode())
    sesion.save()

def actualizar_xml_cierre(usuario):
    try:
        sesion = Sesiones.objects.filter(userID_id=usuario).latest('rideID')

        root = ET.fromstring(sesion.xml)

        timeout = ET.SubElement(root, 'timeout')
        timeout.text = timezone.localtime(timezone.now()).strftime('%H:%M:%S.%f')

        dateout = ET.SubElement(root, 'dateout')
        dateout.text = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')

        sesion.xml = ET.tostring(root, encoding='utf-8').decode()
        sesion.save()
    except Sesiones.DoesNotExist:
        pass

def obtener_direccion_ip_del_usuario(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
