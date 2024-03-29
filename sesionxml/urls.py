from django.urls import path
from . import views

urlpatterns = [
    # Otra rutas de URLs aquí...
    path('user', views.vista_generar_xml_usuario, name='generar_xml_usuario'),
]
