# Generated by Django 5.1.2 on 2024-10-28 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0006_mesa_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
