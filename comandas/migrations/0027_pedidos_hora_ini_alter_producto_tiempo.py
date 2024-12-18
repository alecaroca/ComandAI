# Generated by Django 5.1.3 on 2024-11-18 03:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0026_rename_ptiempo_producto_tiempo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='hora_ini',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='tiempo',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
