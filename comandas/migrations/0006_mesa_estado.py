# Generated by Django 5.1.2 on 2024-10-27 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0005_mesa'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesa',
            name='estado',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
