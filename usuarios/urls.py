from django.urls import path
from .views import crear_usuario, listar_usuarios, editar_usuario, borrar_usuarios, upload_users

urlpatterns = [
    path('crear', crear_usuario , name="crear_usuario" ),
    path('lista', listar_usuarios , name="listar_usuarios" ),
    path('editar/<int:id>', editar_usuario , name="editar_usuario" ),
    path('eliminar/<int:id>', borrar_usuarios , name="borrar_usuarios" ),
    path('cargarusuarios', upload_users , name="cargar_usuarios" ),
]