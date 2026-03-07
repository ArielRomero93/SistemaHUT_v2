import string
import random
from django.db import migrations, models

def generate_codigo_unico(apps, schema_editor):
    FormularioInscripcionHUT = apps.get_model('inscripciones', 'FormularioInscripcionHUT')
    
    for inscripcion in FormularioInscripcionHUT.objects.all():
        if not inscripcion.codigo_acceso:
            while True:
                random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                codigo = f"HUT-{random_chars}"
                if not FormularioInscripcionHUT.objects.filter(codigo_acceso=codigo).exists():
                    inscripcion.codigo_acceso = codigo
                    inscripcion.save(update_fields=['codigo_acceso'])
                    break

def reverse_codigo_unico(apps, schema_editor):
    FormularioInscripcionHUT = apps.get_model('inscripciones', 'FormularioInscripcionHUT')
    FormularioInscripcionHUT.objects.update(codigo_acceso=None)

class Migration(migrations.Migration):
    dependencies = [
        ('inscripciones', '0005_gruposmoodle_participantes_alter_gruposmoodle_dia'),
    ]
    operations = [
        migrations.AddField(
            model_name='formularioinscripcionhut',
            name='codigo_acceso',
            field=models.CharField(blank=True, help_text='Código único para que el alumno acceda a su panel', max_length=15, null=True, unique=True),
        ),
        migrations.RunPython(generate_codigo_unico, reverse_codigo_unico),
    ]
