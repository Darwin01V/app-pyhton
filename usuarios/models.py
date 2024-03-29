from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission 
from django.utils import timezone
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Usuario(AbstractUser):
    session_active = models.BooleanField(default=False)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios')

    def __str__(self):
        return self.username

class RegistroSesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    usuarios = models.ManyToManyField(Usuario)

    def __str__(self):
        return self.nombre

class Sesiones(models.Model):
    rideID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    xml = models.TextField()
    date_create = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Sesión de {self.userID}"
    
    