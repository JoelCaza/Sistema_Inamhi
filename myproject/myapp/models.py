from django.db import models

class MyModel(models.Model):
    codigo_bien = models.CharField(max_length=100, verbose_name='Cod. Bien')
    codigo_anterior = models.CharField(max_length=100, verbose_name='Cod. Anterior')
    codigo_provisional = models.CharField(max_length=100, verbose_name='Cod. Provisional')
    codigo_nuevo = models.CharField(max_length=100, verbose_name='Cod. Nuevo')
    nombre_bien = models.CharField(max_length=100, verbose_name='Nombre Bien')
    serie = models.CharField(max_length=200, verbose_name='Serie')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    color = models.CharField(max_length=50, verbose_name='Color')
    material = models.CharField(max_length=50, verbose_name='Material')
    estado = models.CharField(max_length=50, verbose_name='Estado')
    ubicacion = models.CharField(max_length=100, verbose_name='Ubicacion')
    cedula = models.CharField(max_length=20, verbose_name='Cedula')
    custodio_actual = models.CharField(max_length=150, verbose_name='Custodio Actual')
    observacion = models.TextField(verbose_name='Observacion')
    estado_registro = models.BooleanField(default=True, verbose_name='Estado de Registro')


    def __str__(self):
        return self.nombre_bien
