# Generated by Django 5.1.2 on 2024-11-12 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0021_sucursal_mesa_sucursal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comensales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='telefono',
            field=models.CharField(max_length=12),
        ),
    ]
