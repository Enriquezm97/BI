# Generated by Django 3.2.15 on 2024-03-18 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_empresa_marca_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenedor',
            name='name_bd',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
