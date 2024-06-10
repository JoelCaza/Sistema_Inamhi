from django import forms
from .models import MyModel, CambioCustodio

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo', 'nombre_bien', 
                  'serie', 'modelo', 'marca', 'color', 'material', 'estado', 'ubicacion', 'cedula', 
                  'custodio_actual', 'observacion', 'archivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # Si el registro no existe (es decir, estamos en la creación)
            for field_name in self.fields:
                if field_name != 'archivo':
                    self.fields[field_name].required = False



class CambioCustodioForm(forms.ModelForm):
    class Meta:
        model = CambioCustodio
        fields = ['nuevo_custodio', 'cedula_nuevo_custodio']
