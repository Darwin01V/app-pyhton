from django.http import JsonResponse
from .utils import generar_xml_usuario
from django.contrib.auth.decorators import login_required

@login_required
def vista_generar_xml_usuario(request):
    if request.method == 'GET':
        xml_data = generar_xml_usuario(request)
        return JsonResponse(xml_data)
    else:
        # Manejar otros métodos HTTP según sea necesario
        return JsonResponse({'error': 'Método no permitido'}, status=405)