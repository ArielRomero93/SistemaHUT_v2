import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_confirmacion_inscripcion(inscripcion):
    """
    Envía el email HTML de confirmación de inscripción.
    Recibe la instancia del modelo FormularioInscripcionHUT recién guardada.
    Incluye la información del grupo asignado y el link de WhatsApp.
    """
    try:
        html_body = render_to_string(
            'inscripciones/confirmacion_inscripcion.html',
            {
                'inscripcion': inscripcion,
                'grupo': inscripcion.grupo,
            },
        )

        email = EmailMessage(
            subject='¡Confirmación de Inscripción — HUT 2026!', 
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[inscripcion.email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        logger.info(
            'Email de confirmación enviado a %s (%s %s)',
            inscripcion.email, inscripcion.nombre, inscripcion.apellido,
        )
        return True

    except Exception as e:
        logger.error(
            'Error al enviar email de confirmación a %s: %s',
            inscripcion.email, e,
        )
        return False


def enviar_confirmacion_grupo(inscripcion, grupo):
    """
    Envía el email HTML de confirmación con el link del grupo de WhatsApp.
    Recibe la instancia de la inscripción y el grupo elegido.
    """
    try:
        html_body = render_to_string(
            'inscripciones/confirmacion_grupo.html',
            {
                'inscripcion': inscripcion,
                'grupo': grupo,
            },
        )

        email = EmailMessage(
            subject='¡Ya tienes tu grupo! — HUT 2026', 
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[inscripcion.email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        logger.info(
            'Email de grupo enviado a %s (%s %s) para el grupo %s',
            inscripcion.email, inscripcion.nombre, inscripcion.apellido, grupo.nombre
        )
        return True

    except Exception as e:
        logger.error(
            'Error al enviar email de confirmación de grupo a %s: %s',
            inscripcion.email, e,
        )
        return False
