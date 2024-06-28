from django import forms
from .models import MyModel, CambioCustodio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Por favor, introduzca un nombre de usuario y contraseña correctos. Por favor, note que ambos campos son sensibles a mayúsculas.",
        'inactive': "Esta cuenta está inactiva.",
    }

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2']
        



class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo', 'nombre_bien', 
                  'serie', 'modelo', 'marca', 'color', 'material', 'estado', 'ubicacion', 'cedula', 
                  'custodio_actual', 'observacion', 'archivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # Si el registro no existe (es decir, estamos en la creación)
            # Si el registro no existe (es decir, estamos en la creación)
            for field_name in self.fields:
                if field_name != 'archivo':
                    self.fields[field_name].required = False



class CambioCustodioForm(forms.ModelForm):
    class Meta:
        model = CambioCustodio
        fields = ['nuevo_custodio', 'cedula_nuevo_custodio']
