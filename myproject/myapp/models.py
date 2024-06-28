from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator  # Importa RegexValidator, sirve para validar los campos 
from django.core.exceptions import ValidationError

# Define el validador personalizado
def validate_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Este campo no puede contener números.')

class MyModel(models.Model):
    # Campos del modelo MyModel
    codigo_bien = models.CharField(max_length=50, verbose_name='Código Bien')
    codigo_anterior = models.CharField(max_length=50, verbose_name='Código Anterior', blank=True, null=True)
    codigo_provisional = models.CharField(max_length=50, verbose_name='Código Provisional', blank=True, null=True)
    codigo_nuevo = models.CharField(max_length=50, verbose_name='Código Nuevo', blank=True, null=True)
    nombre_bien = models.CharField(max_length=100, verbose_name='Nombre Bien')
    serie = models.CharField(max_length=50, verbose_name='Serie', blank=True, null=True)
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    custodio_actual = models.CharField(max_length=150, verbose_name='Custodio Actual')
    observacion = models.TextField(verbose_name='Observación', blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/', verbose_name='Archivo Adjunto', blank=True, null=True)
    estado_registro = models.BooleanField(default=True, verbose_name='Estado de Registro')
    cedula = models.CharField (max_length=10, 
        verbose_name='Cédula', 
        validators=[
            RegexValidator(regex=r'^\d{9,10}$', message='La cédula debe tener entre 9 y 10 dígitos y no debe contener letras.'),
            MinLengthValidator(9, message='La cédula debe tener al menos 9 dígitos.')
        ])

    color = models.CharField(
        max_length=50, 
        verbose_name='Color',
        validators=[validate_no_numbers]
    )
    material = models.CharField(
        max_length=50, 
        verbose_name='Material',
        validators=[validate_no_numbers]
    )
    estado = models.CharField(
        max_length=50, 
        verbose_name='Estado',
        validators=[validate_no_numbers]
    )
    ubicacion = models.CharField(
        max_length=100, 
        verbose_name='Ubicación',
        validators=[validate_no_numbers]
    )

    def __str__(self):
        return self.codigo_bien

class CambioCustodio(models.Model):
    modelo_relacionado = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    nuevo_custodio = models.CharField(max_length=150, verbose_name='Nuevo Custodio')
    cedula_nuevo_custodio = models.CharField(
        max_length=10, 
        verbose_name='Cédula Nuevo Custodio', 
        validators=[
            RegexValidator(regex=r'^\d{9,10}$', message='La cédula del nuevo custodio debe tener entre 9 y 10 dígitos y no debe contener letras.'),
            MinLengthValidator(9, message='La cédula del nuevo custodio debe tener al menos 9 dígitos.')
        ]
    )
    fecha_cambio = models.DateField(verbose_name='Fecha de Cambio') 

    def __str__(self):
        return "Cambio de custodio para {self.modelo_relacionado.nombre_bien} el {self.fecha_cambio}"
