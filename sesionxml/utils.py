from usuarios.models import Sesiones, Usuario
import xml.etree.ElementTree as ET
from django.utils import timezone
import xmltodict
import json
from django.http import JsonResponse

def generar_xml_usuario(request):
    user_id = request.session.get('user_id')
    
    try:
        usuario = Usuario.objects.get(id=user_id)
        
        root = ET.Element('user')

        firstname = ET.SubElement(root, 'firstname')
        firstname.text = usuario.persona.nombre
        lastname = ET.SubElement(root, 'lastname')
        lastname.text = usuario.persona.apellido

        sessions = ET.SubElement(root, 'sessions')

        sesiones_usuario = Sesiones.objects.filter(userID_id=user_id)

        for sesion in sesiones_usuario:
            sesion_xml_string = sesion.xml
            sesion_xml_dict = xmltodict.parse(sesion_xml_string)

            sesion_element = ET.SubElement(sessions, 'session')
            
            ip_element = ET.SubElement(sesion_element, 'IP')
            ip_element.text = sesion_xml_dict['session']['ip_address']  
            
            timein_element = ET.SubElement(sesion_element, 'timein')
            timein = timezone.datetime.strptime(sesion_xml_dict['session']['timein'], '%H:%M:%S')
            timein_element.text = timein.strftime('%H:%M:%S')  # Formatear la hora según tu preferencia
            
            datein_element = ET.SubElement(sesion_element, 'datein')
            datein_element.text = timein.strftime('%Y-%m-%d')  # Formatear la fecha según tu preferencia
            
            if 'timeout' in sesion_xml_dict['session']:
                timeout_element = ET.SubElement(sesion_element, 'timeout')
                timeout = timezone.datetime.strptime(sesion_xml_dict['session']['timeout'], '%H:%M:%S.%f')
                timeout_element.text = timeout.strftime('%H:%M:%S')  # Formatear la hora según tu preferencia
            else:
                timeout_element = ET.SubElement(sesion_element, 'timeout')
                timeout_element.text = "Hora de cierre no disponible"
                
            if 'dateout' in sesion_xml_dict['session']:
                dateout_element = ET.SubElement(sesion_element, 'dateout')
                dateout = timezone.datetime.strptime(sesion_xml_dict['session']['dateout'], '%Y-%m-%d')
                dateout_element.text = dateout.strftime('%Y-%m-%d')  # Formatear la fecha según tu preferencia
            else:
                dateout_element = ET.SubElement(sesion_element, 'dateout')
                dateout_element.text = "Fecha de cierre no disponible"


        xml_string = ET.tostring(root, encoding='utf-8')
        xml_dict = xmltodict.parse(xml_string)

        return xml_dict

    except Usuario.DoesNotExist:
        # Si no se encuentra el usuario, devuelve una respuesta de error
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
