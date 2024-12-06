# Generated by Django 5.1.2 on 2024-11-11 23:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0018_rename_fecha_comandas_fecha_ini_remove_comandas_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comandas',
            name='medio_pago',
            field=models.IntegerField(blank=True, choices=[(0, 'Efectivo'), (1, 'Transferencia'), (2, 'Tarjetas')], null=True),
        ),
        migrations.AlterField(
            model_name='comandas',
            name='mesa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comandas.mesa'),
        ),
        migrations.AlterField(
            model_name='comandas',
            name='mesero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mesa',
            name='capacidad',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mesa',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(0, 'Libre'), (1, 'Ocupado')], null=True),
        ),
        migrations.AlterField(
            model_name='mesa',
            name='ubicacion',
            field=models.IntegerField(blank=True, choices=[(0, '1er piso'), (1, '2er piso'), (2, '3er piso'), (3, 'terraza')], null=True),
        ),
    ]
