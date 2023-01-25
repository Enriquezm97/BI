# Generated by Django 3.2.15 on 2022-11-18 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('formula', models.CharField(max_length=150)),
                ('rango_desde_1', models.FloatField(null=True)),
                ('rango_hasta_1', models.FloatField(null=True)),
                ('rango_color_1', models.CharField(max_length=7, null=True)),
                ('rango_desde_2', models.FloatField(null=True)),
                ('rango_hasta_2', models.FloatField(null=True)),
                ('rango_color_2', models.CharField(max_length=7, null=True)),
                ('rango_desde_3', models.FloatField(null=True)),
                ('rango_hasta_3', models.FloatField(null=True)),
                ('rango_color_3', models.CharField(max_length=7, null=True)),
                ('ejex', models.CharField(max_length=50, null=True)),
                ('ejey', models.CharField(max_length=50, null=True)),
                ('valor_minimo', models.FloatField(null=True)),
                ('valor_maximo', models.FloatField(null=True)),
                ('dataframe', models.CharField(max_length=150, null=True)),
                ('indicador_tipo', models.CharField(choices=[('Liquidez', 'Liquidez'), ('Rentabilidad', 'Rentabilidad'), ('Solvencia', 'Solvencia')], default='Rentabilidad', max_length=50)),
                ('indicador_favorito', models.BooleanField(default=False)),
                ('indicador_comentario', models.CharField(max_length=500, null=True)),
                ('tipo_graph', models.CharField(max_length=50, null=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.usuario')),
            ],
        ),
    ]