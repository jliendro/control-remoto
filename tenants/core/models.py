from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    telefono = models.CharField(max_length=200)
    pass


class Inquilino(User):
    CBU = models.IntegerField()
    #foto

    def fecha_ingreso():
        pass


class Garante(User):
    CBU = models.IntegerField()
    #foto
    pass


class Pago(models.Model):
    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT)
    fecha_de_cobro = models.DateTimeField()
    fecha_de_pago = models.DateTimeField(null=True, blank=True)
    monto = models.IntegerField()
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    # adjunto


class ContactoLaboral(User):
    descripcion = models.CharField(max_length=300, null=True, blank=True)


class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    altura = models.IntegerField()
    ciudad = models.CharField(max_length=100)
    codigopostal = models.CharField(max_length=10, null=True, blank=True)
    # geolocalizacion


class Lugar(models.Model):
    PISOS = {'0': 'PB',
             '1': '1',
             '2': '2',
             '3': '3',
             '4': '4',
             '5': '5',
             '6': '6',
             '7': '7',
             '8': '8',
             '9': '9',
             '10': '10'}

    CIUDAD = {'B': 'Buenos Aires',
              'S': 'Salta',
              'M': 'Mar del Plata'}

    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    piso = models.CharField(max_length=1, choices=PISOS.items())
    departamento = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=1, choices=CIUDAD.items())


class Contrato(models.Model):
    UNIDADES = {'E': 'pesos', 'O': 'porcentaje'}

    fecha_firma = models.DateTimeField(null=True, blank=True,
                                       verbose_name="Fecha de Firma")

    fecha_desde = models.DateTimeField(null=True, blank=True,
                                       verbose_name="Fecha de inicio")
    fecha_hasta = models.DateTimeField(null=True, blank=True,
                                       verbose_name="Fecha de fin")

    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT,
                                  related_name="inquilino")
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT,
                              verbose_name="Lugar alquilado")
    interes_diario = models.IntegerField()
    unidad_interes = models.CharField(max_length=1, choices=UNIDADES.items())
    garantes = models.ForeignKey(Garante, on_delete=models.PROTECT)

    firmado = models.BooleanField(verbose_name="Firmado con puño y letra")

    administrador = models.ForeignKey(User, on_delete=models.PROTECT,
                                      verbose_name="Administrador Local",
                                      null=True, blank=True,
                                      related_name="administrador")
    contacto_laboral = models.ForeignKey(ContactoLaboral,
                                         on_delete=models.PROTECT,
                                         null=True, blank=True,
                                         related_name="contacto_laboral")
    valor_dolar = models.DecimalField(max_digits=5, decimal_places=2,
                                      verbose_name="Valor de dólar al momento \
                                                    de la firma del contrato")


class MontoContrato(models.Model):
    cantidad = models.DecimalField(max_digits=5, decimal_places=2,
                                   verbose_name="Precio alquiler")
    fecha_desde = models.DateTimeField(verbose_name="Desde que fecha se \
                                                     comienza a cobrar este \
                                                     precio")
    description = models.CharField(max_length=200, null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)


class Observacion(models.Model):
    fecha = models.DateTimeField()
    description = models.CharField(max_length=200)
    costos_asociados = models.DecimalField(max_digits=5, decimal_places=2,
                                           verbose_name="Costo asociado a la \
                                                         observación",
                                           null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
