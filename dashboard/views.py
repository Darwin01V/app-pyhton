from django.shortcuts import render
from usuarios.models import Usuario, Persona,RegistroSesion

# Create your views here.
def home(request):
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(id=user_id)
    sesiones = RegistroSesion.objects.filter(usuario_id=user_id).order_by('-fecha_inicio')
    return render(request, 'dashboard.html', {'usuario': usuario , 'sesiones': sesiones})