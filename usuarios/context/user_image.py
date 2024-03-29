from ..models import Usuario
from ..utils import obtener_imagen_pokemon
def user_image(request):
    imagen_url = None
    if request.user.is_authenticated:
        numero = request.session.get('user_id')
        imagen_url = obtener_imagen_pokemon(numero)  # Ajusta esto según tu modelo de Usuario

    # Devuelve un diccionario con la URL de la imagen del usuario
    return {'imagen_url': imagen_url}