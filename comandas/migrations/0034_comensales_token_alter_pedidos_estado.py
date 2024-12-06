# Generated by Django 5.1.3 on 2024-11-29 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0033_merge_20241123_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='comensales',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(0, 'preparacion'), (1, 'entregado'), (2, 'preparado'), (3, 'marcado'), (4, 'confirmar')], null=True),
        ),
    ]
