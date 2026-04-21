from django.core.management.base import BaseCommand
from inscripciones.models import FormularioInscripcionHUT
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import time

class Command(BaseCommand):
    help = 'Reenvía por correo el código único y link de acceso solo a los correos que fallaron en el envío anterior'

    def handle(self, *args, **kwargs):
        # Lista de correos que fallaron extraída de los logs del servidor
        correos_fallidos = [
            'ruth.noriega.elizabeth@gmail.com', 'diegorojasledezma@gmail.com', 'samy.564@hotmail.com',
            'micalalfonso23@gmail.com', 'eduardopachecoc@gmail.com', 'smarcos0712@gmail.com',
            'keila.szkarlatiuk@mi.unc.edu.ar', 'anubisstudies@gmail.com', 'keilaortiz070@gmail.com',
            'noeliamartelingrid@gmail.com', 'rebex1ross@gmail.com', 'albaruthramirez1@gmail.com',
            'vicdele1971@gmail.com', 'pereyradiazisabel@gmail.com', 'dulciata07@gmail.com',
            'adrianelec1@gmail.com', 'katypolischuk@gmail.com', 'eduardoeduardo1010@hotmail.com',
            'brendy9700@gmail.com', 'joanabelenmendez@gmail.com', 'dire0286@hotmail.com',
            'isabellapino01@gmail.com', 'micaclarisego@gmail.com', 'mikaelaalmiron200@gmail.com',
            'danielariverosdaniela@gmail.com', 'tiinasmit@gmail.com', 'ambaritototo@gmail.com',
            'daironzapata510@gmail.com', 'gilmdayan41@gmail.com', 'florencia.traibermin@gmail.com',
            'jonatankilly@gmail.com', 'melyfuertes@gmail.com', 'hernandezpaulaluz@gmail.com',
            'Gomedia.jose@gmail.com', 'rosalyndiaz2026@gmail.com', 'mairasantillan40@gmail.com',
            'consultorarobert@gmail.com', 'ciontosclaudiu@gmail.com', 'constanzawikel@gmail.com',
            'cocachcamila@gmail.com', 'katheurregog@gmail.com', 'alcarolek@gmail.com',
            'diana.valeria.c28@gmail.com', 'eveysaleudo0403@gmail.com', 'lenymontoyac@gmail.com',
            'deborahpacheco602@gmail.com', 'marcelo_vera@hotmail.com', 'fernandezseleneana@gmail.com',
            'eve.sinner.vera@gmail.com', 'narazarlenga@gmail.com', 'gabitagliavini@hotmail.com',
            'anacarinalopez849@gmail.com', 'dranataliatamagna@gmail.com', 'marukvil@gmail.com',
            'tolabagal.so@gmail.com', 'miriamvveron@gmail.com', 'marielvillablanca@gmail.com',
            'lucycarrizo.99@gmail.com', 'riosvildozanahiragustina@gmail.com', 'marry34@hotmail.com.ar',
            'jesicamolins@hotmail.com', 'nazacuello76@gmail.com', 'arandanatalia288@gmail.com',
            'lorena94jorge@gmail.com', 'aniipau7@gmail.com', 'jfernandezmillicay@gmail.com',
            'rociosol789@gmail.com', 'tomasolmos735@gmail.com', 'fierrho07@gmail.com',
            'soldanluz@gmail.com', 'julianaespinoza002@gmail.com', 'camarivjimenez@gmail.com',
            'biancacacha007@gmail.com', 'luzmelinac12@gmail.com', 'mauricionazarenovargas@gmail.com',
            'estefania10141984@icloud.com', 't68252242@gmail.com', 'lulisandoval2@gmail.com',
            'jev.torrente@gmail.com', 'nahiaraamarilla66@gmail.com', 'gisellerios.com.ar@gmail.com',
            'pau.b.p22@gmail.com', 'nefertitis.vs.3@gmail.com', 'erikavicente1999@gmail.con',
            'keilajazminszk@gmail.com', 'joaqcastroo@gmail.com', 'estebanabraham@gmail.com',
            'lucianam.piriz@gmail.com'
        ]

        # Convertir a minúsculas por las dudas para que coincida con la BD
        correos_fallidos = [email.lower() for email in correos_fallidos]

        # Buscamos en la base de datos las inscripciones que tengan esos correos
        inscriptos = FormularioInscripcionHUT.objects.filter(email__in=correos_fallidos, codigo_acceso__isnull=False)
        total = inscriptos.count()
        enviados = 0

        self.stdout.write(self.style.WARNING(f'Iniciando reenvío de códigos a {total} inscriptos (con límite de velocidad)...'))

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
                
                # PAUSA de 2 segundos para evitar bloqueo de conexión
                time.sleep(2)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al enviar a {inscripcion.email}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Proceso completado. Se enviaron {enviados} de {total} correos.'))
