from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

class Inquilino(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # usuario (nombre, apellido, email, celphone)
    # fecha_ingreso
    # fecha_egreso
	# telefono
	# foto


class Pago(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # inquilino
    # fecha_de_pago
    # monto
    # estado

class ContactoLaboral(models.Model):
	# usuario
	# nombre de lugar
	# cargo

class Monto(models.Model):
	# cantidad
	# fecha desde
	# fecha hasta

class Contrato(models.Model):
	# inquilino
	# interes_por_mora_por_dia
	# garantes
	# firmado
	# fecha de firma
	# responsable_local
	# contacto_laboral
	# montos
	# observaciones

class Direccion(models.Model):
	calle = models.CharField(max_length=100)
	altura = models.IntegerField()
	ciudad = models.CharField(max_length=100)

class Lugar(models.Model):
	direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
	piso = models.IntegerField()
	departamento = models.IntegerField()


class Observación(models.Model):
	# inquilino
	# description
	# costos_asociados