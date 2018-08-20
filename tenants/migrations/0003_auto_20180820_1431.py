# Generated by Django 2.1 on 2018-08-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_auto_20180820_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='valor_dolar',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor de dólar al momento                                                     de la firma del contrato'),
        ),
        migrations.AlterField(
            model_name='montocontrato',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Precio alquiler'),
        ),
        migrations.AlterField(
            model_name='observacion',
            name='costos_asociados',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Costo asociado a la                                                          observación'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
