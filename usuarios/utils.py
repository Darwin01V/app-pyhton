# utils.py
from openpyxl import load_workbook
from .models import Persona, Rol, Usuario

def process_excel_file(uploaded_file):
    users_created = 0
    wb = load_workbook(uploaded_file)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        nombre, apellido, identificacion, fecha_nacimiento, correo, username, password, rol_nombre = row
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
            nombre=nombre.lower().capitalize(),
            apellido=apellido.lower().capitalize(),
            identificacion=identificacion.lower(),
            fecha_nacimiento=fecha_nacimiento
        )
        
        # Crear o obtener el rol
        rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)
        
        # Crear el usuario
        user = Usuario.objects.create_user(
            username=username,
            email=correo,
            password=password,
            first_name=nombre.lower().capitalize(),
            last_name=apellido.lower().capitalize()
        )
        
        # Asignar la persona al usuario
        user.persona = persona
        user.save()
        
        # Asignar el rol al usuario a través de la tabla intermedia
        rol.usuarios.add(user)
        
        users_created += 1
    
    return users_created
