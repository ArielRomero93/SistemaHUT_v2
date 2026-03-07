from django.core.management.base import BaseCommand
from inscripciones.models import FormularioInscripcionHUT
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Command(BaseCommand):
    help = 'Envía por correo el código único y link de acceso a inscriptos existentes que aún no lo han recibido'

    def handle(self, *args, **kwargs):
        inscriptos = FormularioInscripcionHUT.objects.filter(codigo_acceso__isnull=False)
        total = inscriptos.count()
        enviados = 0

        self.stdout.write(self.style.WARNING(f'Iniciando envío de códigos a {total} inscriptos...'))

        for inscripcion in inscriptos:
            try:
                # Todo: Reemplazar con URL de producción real o usar Site de Django si está configurado
                host = 'http://127.0.0.1:8000' 
                link_acceso = f"{host}/mi-grupo/"
                
                context = {
                    'inscripcion': inscripcion,
                    'codigo_acceso': inscripcion.codigo_acceso,
                    'link_acceso': link_acceso
                }
                
                html_message = render_to_string('emails/codigo_acceso_antiguo.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject='Tu Código de Acceso Único - Sistema HUT',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inscripcion.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                enviados += 1
                self.stdout.write(self.style.SUCCESS(f'Enviado a {inscripcion.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al enviar a {inscripcion.email}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Proceso completado. Se enviaron {enviados} de {total} correos.'))
