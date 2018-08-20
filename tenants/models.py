from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    telefono = models.CharField(max_length=200)

    tipo_documento = models.CharField(max_length=100, null=True, blank=True)
    documento_numero = models.IntegerField(null=True, blank=True)
    pais_nacimiento = models.CharField(max_length=100, default="Argentina")
    fecha_nacimiento = models.DateField(null=True, blank=True)


class Inquilino(User):
    CBU = models.IntegerField()

    def __str__(self):
        return "{}, {}".format(self.last_name.title(), self.first_name.title())

    class Meta:
        # Admin porpuse
        verbose_name = "Inquilino"

    def fecha_ingreso():
        pass

    def activo(self):
        return Contrato.objects.filter(inquilino=self,
                                       fecha_hasta__gte=timezone.now()) \
                               .exists()
    activo.boolean = True


class Garante(User):
    CBU = models.IntegerField()

    class Meta:
        # Admin porpuse
        verbose_name = "Garante"

    def __str__(self):
        return "{}, {}".format(self.last_name.title(), self.first_name.title())

    def activo(self):
        return Contrato.objects.filter(garantes=self,
                                       fecha_hasta__gte=timezone.now()) \
                               .exists()
    activo.boolean = True


class Pago(models.Model):
    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT)
    fecha_de_cobro = models.DateField()
    fecha_de_pago = models.DateField(null=True, blank=True)
    monto = models.DecimalField(max_digits=7, decimal_places=2,)

    descripcion = models.CharField(max_length=200, null=True, blank=True)
    # adjunto

    def origen(self):
        return Lugar.objects.filter(contrato__inquilino=self.inquilino) \
                            .order_by('-contrato__fecha_hasta').first()


class ContactoLaboral(User):
    descripcion = models.CharField(max_length=300, null=True, blank=True)


class Direccion(models.Model):

    class Meta:
        verbose_name_plural = "Direcciones"

    calle = models.CharField(max_length=100)
    altura = models.IntegerField()
    ciudad = models.CharField(max_length=100)
    codigopostal = models.CharField(max_length=10, null=True, blank=True)
    # geolocalizacion

    def __str__(self):
        return "{} {}".format(self.calle.title(), self.altura)


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

    class Meta:
        verbose_name_plural = "Propiedades"

    def __str__(self):
        return "{} - {} - {}".format(self.direccion.ciudad,
                                     self.direccion,
                                     self.ubicacion)

    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    piso = models.CharField(max_length=1, choices=PISOS.items())
    departamento = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    @property
    def ubicacion(self):
        nota = '{} '.format(Lugar.PISOS[self.piso])
        if self.departamento:
            nota += "Dpto {}".format(self.departamento)
        if self.descripcion:
            nota += self.descripcion
        return nota


class Contrato(models.Model):
    UNIDADES = {'E': 'pesos', 'O': 'porcentaje'}

    fecha_firma = models.DateField(null=True, blank=True,
                                       verbose_name="Fecha de Firma")

    fecha_desde = models.DateField(null=True, blank=True,
                                       verbose_name="Fecha de inicio")
    fecha_hasta = models.DateField(null=True, blank=True,
                                       verbose_name="Fecha de fin")

    inquilino = models.ForeignKey(Inquilino, on_delete=models.PROTECT,
                                  related_name="inquilino")
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT,
                              verbose_name="Propiedad")
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
    valor_dolar = models.DecimalField(max_digits=7, decimal_places=2,
                                      verbose_name="Valor de dólar al momento \
                                                    de la firma del contrato")

    def activo(self):
        if not self.fecha_hasta:
            return False
        return self.fecha_hasta >= timezone.now()
    activo.boolean = True


class MontoContrato(models.Model):
    cantidad = models.DecimalField(max_digits=7, decimal_places=2,
                                   verbose_name="Precio alquiler")
    fecha_desde = models.DateField(verbose_name="Desde que fecha se \
                                                     comienza a cobrar este \
                                                     precio")
    description = models.CharField(max_length=200, null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)


class Observacion(models.Model):
    fecha = models.DateField()
    description = models.CharField(max_length=200)
    costos_asociados = models.DecimalField(max_digits=7, decimal_places=2,
                                           verbose_name="Costo asociado a la \
                                                         observación",
                                           null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
