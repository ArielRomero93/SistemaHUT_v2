from django.db import migrations, models
import django.db.models.deletion


def crear_cursos_y_asignar(apps, schema_editor):
    """Crea CursoHUT 1 y 2, asigna el 1 a todos los inscriptos existentes."""
    CursoHUT = apps.get_model('inscripciones', 'CursoHUT')
    FormularioInscripcionHUT = apps.get_model('inscripciones', 'FormularioInscripcionHUT')

    # Crear los dos cursos
    curso1 = CursoHUT.objects.create(pk=1, nombre='HUT 1', anio=2025, activo=False)
    curso2 = CursoHUT.objects.create(pk=2, nombre='HUT 2', anio=2026, activo=True)

    # Asignar curso 1 a todas las inscripciones existentes
    FormularioInscripcionHUT.objects.filter(curso__isnull=True).update(curso=curso1)


class Migration(migrations.Migration):

    dependencies = [
        ('inscripciones', '0001_initial'),
    ]

    operations = [
        # 1. Crear tabla CursoHUT
        migrations.CreateModel(
            name='CursoHUT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Curso')),
                ('anio', models.IntegerField(verbose_name='Año')),
                ('activo', models.BooleanField(default=False, verbose_name='Habilitado')),
            ],
            options={
                'verbose_name': 'Curso HUT',
                'verbose_name_plural': 'Cursos HUT',
                'ordering': ['-anio'],
            },
        ),
        # 2. Agregar campo curso como NULLABLE primero
        migrations.AddField(
            model_name='formularioinscripcionhut',
            name='curso',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='inscripciones.cursohut',
                verbose_name='Curso HUT',
            ),
            preserve_default=False,
        ),
        # 3. Crear cursos y asignar HUT 1 a existentes
        migrations.RunPython(crear_cursos_y_asignar, migrations.RunPython.noop),
        # 4. Hacer el campo NOT NULL ahora que todos tienen valor
        migrations.AlterField(
            model_name='formularioinscripcionhut',
            name='curso',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='inscripciones.cursohut',
                verbose_name='Curso HUT',
            ),
        ),
    ]
