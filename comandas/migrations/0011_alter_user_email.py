# Generated by Django 5.1.2 on 2024-10-28 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comandas', '0010_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
