# Generated by Django 3.2.15 on 2023-09-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230929_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='name_empresa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
