# Generated by Django 4.0.5 on 2022-09-15 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyectos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjetivoX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enPapelera', models.BooleanField(default='False')),
                ('fechaPapelera', models.DateField(blank=True, null=True)),
                ('fechaCreacion', models.DateField(auto_now_add=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('general', models.BooleanField(verbose_name=False)),
                ('proyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyectos.proyecto')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
