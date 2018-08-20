# Generated by Django 2.1 on 2018-08-20 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='documento_numero',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='fecha_nacimiento',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='pais_nacimiento',
            field=models.CharField(default='Argentina', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='tipo_documento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
