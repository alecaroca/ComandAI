# Generated by Django 5.1.3 on 2024-11-19 04:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0026_rename_ptiempo_producto_tiempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comandas',
            name='mesa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comandas.mesa'),
        ),
        migrations.AlterField(
            model_name='comandas',
            name='mesero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]