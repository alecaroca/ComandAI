# Generated by Django 5.1.3 on 2024-11-20 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0030_alter_pedidos_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(0, 'preparacion'), (1, 'entregado'), (2, 'pendiente'), (3, 'marcado')], null=True),
        ),
    ]
