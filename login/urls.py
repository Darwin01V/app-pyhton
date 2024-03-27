from django.urls import path
from .views import iniciar_sesion, cerrar_sesion

urlpatterns = [
    path('', iniciar_sesion , name="iniciar_sesion"),
    path('login', iniciar_sesion , name="iniciar_sesionr"),
    path('cerrar', cerrar_sesion , name="cerrar_sesion"),
]