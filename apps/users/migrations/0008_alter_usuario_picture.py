# Generated by Django 3.2.15 on 2024-02-19 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_usuario_datos_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='picture',
            field=models.BinaryField(null=True),
        ),
    ]
