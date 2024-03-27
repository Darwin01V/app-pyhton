# forms.py
from django import forms

class UserUploadForm(forms.Form):
    file = forms.FileField(label='Seleccionar archivo Excel (.xlsx)')
