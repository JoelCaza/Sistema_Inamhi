from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model = MyModel
        fields = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo', 'nombre_bien', 'serie', 'modelo', 'marca', 'color', 'material', 'estado', 'ubicacion', 'cedula', 'custodio_actual', 'observacion', 'archivo']
