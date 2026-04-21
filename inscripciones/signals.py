from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AreaInteres, TerminosCondiciones

AREAS_DE_INTERES_INICIALES = [
    "Diseño (Uso profesional de canva, Adobe Photoshop, Adobe Illustrator,)",
    "Contenido en redes (Creación de contenido para la publicación, escritura en Redes, conocimiento de Community Manager, Content Manager, para redes sociales)",
    "Sistemas (Creación de programas web, diseño web, seguridad digital)",
    "Movilizador de Reacciona ( Se necesita haber realizado el curso Reacciona)",
    "Stand (Posibilidad de estar en los stand en eventos misioneros en tu ciudad)",
    "Editor/a, productor/a de videos (Diseño y edición de videos para YouTube, Instagram y programas de capacitación de Fronteras)",
    "Traducción (Traducción de documentos del ingles al español o del español al ingles u otro idioma)",
    "HUT (Tutor/a, Realización de actividades especiales de manera virtual para estudiantes)",
    "Profesional al Servicio del campo (Psicología, trabajo social, medicina, Abogacía, etc)",
    "Revisión de redacción, documentos, ortografía, corrección de textos, elaboración de materiales teóricos, cursos.",
    "Secretaria (Llevar agenda de cumpleaños de obreros, generar y enviar tarjetita de saludo; apoyo en el área, Envio de saludos en fechas especiales como pascuas, navidad, etc)"
]

TERMINOS_VOLUNTARIO = """<p><strong>1. Compromiso Voluntario:</strong> Me comprometo a prestar servicio en Fronteras Argentina como voluntario/a sin relación laboral, pudiendo realizar las actividades seleccionadas con el objetivo de lograr los fines para los que la organización está destinada.</p>
<p><strong>2. Sin Vínculo Laboral:</strong> Soy plenamente consciente de que la prestación de los servicios aquí propuestos no genera un vínculo laboral, ni una obligación de derechos laborales, de seguridad social, hereditarios o similares entre mi persona y Fronteras Argentina.</p>
<p><strong>3. Normas y Desvinculación:</strong> Me comprometo a realizar las actividades propuestas por el/la responsable del área de servicio y a seguir las normativas de la organización. Entiendo que el incumplimiento de las normas o la ocurrencia de conductas inapropiadas pueden causar mi desvinculación inmediata del voluntariado.</p>
<p><strong>4. Responsabilidad de Gastos y Daños:</strong> Me comprometo a cubrir todos los gastos personales relacionados con mis actividades, excepto en situaciones donde Fronteras Argentina, por acuerdo previo y por escrito, confirme que cubrirá gastos específicos. Soy consciente de que Fronteras Argentina no será responsable de ningún daño moral, material o físico que pueda ocurrirme durante el desempeño de mis actividades voluntarias.</p>"""

@receiver(post_migrate)
def poblar_datos_iniciales(sender, **kwargs):
    if sender.name == 'inscripciones':
        for area in AREAS_DE_INTERES_INICIALES:
            AreaInteres.objects.get_or_create(nombre=area)

        # Términos y Condiciones - solo Voluntario por ahora.
        # Para agregar Candidato o Interesado, agregar más líneas aquí.
        TerminosCondiciones.objects.get_or_create(
            rol='VOLUNTARIO',
            defaults={'texto_html': TERMINOS_VOLUNTARIO}
        )
