from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo', 'nombre_bien', 'serie', 'modelo', 'marca', 'color', 'material', 'estado', 'ubicacion', 'cedula', 'custodio_actual', 'observacion']
