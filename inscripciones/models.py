from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import os


# ======================
# USUARIOS
# ======================

class Usuario(models.Model):
    ROLES = (
        (1001, 'Super'),
        (2002, 'Directivo'),
        (3003, 'Coordinador'),
        (111111, 'Desautorizado'),
    )

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLES)
    reset_token = models.CharField(max_length=100, blank=True, null=True)

    ultimoIngreso = models.DateTimeField(default=timezone.now)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.ultimoIngreso = timezone.now()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# ======================
# MENU
# ======================

class OpcionesMenu(models.Model):
    TIPOS_OPCION = (
        (1, 'Reportes'),
        (2, 'Formulario'),
        (3, 'Gráficos'),
    )

    Codigo = models.CharField(max_length=50, unique=True)
    Descripcion = models.CharField(max_length=100)
    Icono = models.CharField(max_length=100)
    TipoOpcion = models.IntegerField(choices=TIPOS_OPCION)
    ruta = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Descripcion

    class Meta:
        verbose_name = 'Opción de Menú'
        verbose_name_plural = 'Opciones de Menú'


# ======================
# UBICACION
# ======================

class Pais(models.Model):
    paisNombre = models.CharField(max_length=100)

    class Meta:
        ordering = ['paisNombre']
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.paisNombre


class ProvinciaEstado(models.Model):
    idPais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provinciaNombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Provincia/Estado'
        verbose_name_plural = 'Provincias/Estados'

    def __str__(self):
        return self.provinciaNombre


# ======================
# CURSOS HUT
# ======================

class CursoHUT(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Curso')
    anio = models.IntegerField(verbose_name='Año')
    activo = models.BooleanField(default=False, verbose_name='Habilitado')

    def __str__(self):
        return f"{self.nombre} ({self.anio})"

    class Meta:
        verbose_name = 'Curso HUT'
        verbose_name_plural = 'Cursos HUT'
        ordering = ['-anio']


def get_curso_activo():
    """Devuelve el PK del curso activo para usarlo como default."""
    curso = CursoHUT.objects.filter(activo=True).first()
    return curso.pk if curso else None

class GruposMoodle(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Grupo')
    curso = models.ForeignKey(CursoHUT, on_delete=models.PROTECT, verbose_name='Curso HUT')
    horario = models.CharField(max_length=100, verbose_name='Horario')
    dia = models.CharField(max_length=15, choices=DIAS_SEMANA, verbose_name='Día')
    tutor = models.CharField(max_length=100, verbose_name='Tutor')
    url_whatsapp = models.URLField(max_length=200, blank=True, null=True, verbose_name='URL WhatsApp')
    capacidad = models.IntegerField(default=8, verbose_name='Capacidad')
    participantes = models.IntegerField(default=0, verbose_name='Participantes')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Grupo Moodle'
        verbose_name_plural = 'Grupos Moodle'
        ordering = ['-fecha_creacion']

# ======================
# FORMULARIO INSCRIPCION
# ======================

class FormularioInscripcionHUT(models.Model):
    ESTADO = (
        ('Soltera/o', 'Soltera/o'),
        ('Casada/o', 'Casada/o'),
    )

    curso = models.ForeignKey(
        CursoHUT,
        on_delete=models.CASCADE,
        verbose_name='Curso HUT',
        default=get_curso_activo,
    )

    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=25)

    edad = models.IntegerField(
        validators=[
            MaxValueValidator(99),
            MinValueValidator(13),
        ]
    )

    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provincia = models.ForeignKey(ProvinciaEstado, on_delete=models.CASCADE)

    ciudad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    congregacion = models.CharField(max_length=50)
    pastor = models.CharField(max_length=50)
    email = models.EmailField()

    estadoCivil = models.CharField(
        choices=ESTADO,
        max_length=9,
        verbose_name='Estado Civil'
    )

    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    abandonado = models.BooleanField(default=False)
    fecha_abandono = models.DateTimeField(blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    grupo = models.ForeignKey(GruposMoodle, on_delete=models.PROTECT, verbose_name='Grupo Moodle', blank=True, null=True)
    codigo_acceso = models.CharField(max_length=8, unique=True, null=True, blank=True, help_text="Código único para que el alumno acceda a su panel")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Inscripción HUT'
        verbose_name_plural = 'Inscripciones HUT'
        ordering = ['-fecha_creacion']


# ======================
# FORMULARIO DECISION
# ======================

class FormularioDeDecision(models.Model):
    OPORTUNIDAD_SERVICIO = (
        ('Voluntariado de Base', 'Voluntariado de Base'),
        ('Candidato a salir al campo', 'Candidato a salir al campo'),
        ('Intercesion', 'Intercesion'),
        ('Futuros tutores de HUT', 'Futuros tutores de HUT'),
        ('Movilizador', 'Movilizador')
    )

    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    profesionOcupacion = models.CharField(max_length=30)
    servicioElegido = models.CharField(choices=OPORTUNIDAD_SERVICIO, max_length=30)

    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Formulario de Decisión'
        verbose_name_plural = 'Formularios de Decisión'


# ======================
# VOLUNTARIOS
# ======================

SI_NO = [
    ('SI', 'Sí'),
    ('NO', 'No'),
]

SI_NO_TALVEZ = [
    ('SI', 'Sí'),
    ('NO', 'No'),
    ('NO_POR_AHORA', 'No por ahora'),
    ('CORTO_PLAZO', 'Por corto plazo'),
]

REALIZO_HUT = [
    ('SI', 'Sí'),
    ('TODAVIA_NO', 'Todavía no'),
]

REALIZO_REACCIONA = [
    ('SI', 'Sí'),
    ('TODAVIA_NO', 'Todavía no'),
]

NIVEL_ESTUDIO = [
    ('PRIMARIA_COMPLETA', 'Primaria completa'),
    ('SECUNDARIA_INCOMPLETA', 'Secundaria incompleta'),
    ('SECUNDARIA_COMPLETA', 'Secundaria completa'),
    ('TERCIARIO_INCOMPLETO', 'Terciario incompleto'),
    ('TERCIARIO_COMPLETO', 'Terciario completo'),
    ('UNIVERSITARIO_INCOMPLETO', 'Universitario incompleto'),
    ('UNIVERSITARIO_COMPLETO', 'Universitario completo'),
]


def validar_extension_imagen(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in ['.jpg', '.jpeg', '.png']:
        raise ValidationError('Solo se permiten imágenes JPG o PNG.')


class AreaInteres(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área de Interés'
        verbose_name_plural = 'Áreas de Interés'


class Voluntario(models.Model):
    ROL_AGENCIA = [
        ('CANDIDATO', 'Candidato'),
        ('VOLUNTARIO', 'Voluntario'),
        ('INTERESADO', 'Interesado'),
    ]

    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    fecha_nacimiento = models.DateField()

    pais_origen = models.CharField(max_length=100, blank=True, null=True)
    pais_residencia = models.CharField(max_length=100, blank=True, null=True)
    provincia_residencia = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True, null=True)

    hijos = models.CharField(max_length=10, choices=SI_NO, default='NO')
    fechas_nacimiento_hijos = models.TextField(blank=True, help_text="Ej: Juan (12-05-2015)")
    con_quien_convive = models.CharField(max_length=255, blank=True, null=True)
    nombre_pastor = models.CharField(max_length=255, blank=True, null=True)
    telefono_pastor = models.CharField(max_length=100, blank=True, null=True)
    rol_agencia = models.CharField(max_length=30, choices=ROL_AGENCIA, blank=True, null=True)

    miembro_iglesia = models.CharField(max_length=10, choices=SI_NO, blank=True, null=True)
    cual_iglesia = models.CharField(max_length=255, blank=True)

    sirve_en_iglesia = models.CharField(max_length=10, choices=SI_NO, blank=True, null=True)
    cual_servicio = models.CharField(max_length=255, blank=True)

    tiempo_asistiendo = models.CharField(max_length=100, blank=True)

    voluntario_otra_org = models.CharField(max_length=10, choices=SI_NO, blank=True, null=True)
    cual_org = models.CharField(max_length=255, blank=True)

    hizo_hut = models.CharField(max_length=20, choices=REALIZO_HUT)
    hizo_hut_anio = models.CharField(max_length=255, blank=True, null=True)
    hizo_reacciona = models.CharField(max_length=20, choices=REALIZO_REACCIONA)
    cuando_reacciona = models.CharField(max_length=255, blank=True, null=True)

    deseo_salir_campo = models.CharField(max_length=30, choices=SI_NO_TALVEZ, blank=True, null=True)

    nivel_estudio = models.CharField(max_length=30, choices=NIVEL_ESTUDIO, blank=True, null=True)
    titulo_universitario = models.CharField(max_length=255, blank=True, null=True)

    cursos_formacion = models.TextField(blank=True)
    experiencia_profesional = models.TextField(blank=True)

    habla_idioma = models.CharField(max_length=10, choices=SI_NO, blank=True, null=True)
    cual_idioma = models.CharField(max_length=255, blank=True, null=True)
    lee_escribe_idioma = models.CharField(max_length=10, choices=SI_NO, blank=True, null=True)
    cual_idioma_lee_escribe = models.CharField(max_length=255, blank=True, null=True)

    areas_interes = models.ManyToManyField(AreaInteres, blank=True)
    otras_propuestas = models.TextField(blank=True, null=True)

    foto_rostro = models.ImageField(
        upload_to='fotos_rostro/',
        validators=[validar_extension_imagen],
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Voluntario'
        verbose_name_plural = 'Voluntarios'


class TerminosCondiciones(models.Model):
    rol = models.CharField(max_length=30, choices=Voluntario.ROL_AGENCIA, unique=True)
    texto_html = models.TextField(help_text="Texto HTML para los términos y condiciones de este rol.")

    def __str__(self):
        return f"Términos para {self.get_rol_display()}"

    class Meta:
        verbose_name = 'Términos y Condiciones'
        verbose_name_plural = 'Términos y Condiciones'


from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

def recalcular_participantes_grupo(grupo):
    if grupo:
        grupo.participantes = FormularioInscripcionHUT.objects.filter(grupo=grupo).count()
        grupo.save(update_fields=['participantes'])

def generar_codigo_unico():
    import random
    import string
    while True:
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        codigo = f"HUT-{random_chars}"
        if not FormularioInscripcionHUT.objects.filter(codigo_acceso=codigo).exists():
            return codigo

@receiver(pre_save, sender=FormularioInscripcionHUT)
def operaciones_pre_save_inscripcion(sender, instance, **kwargs):
    if not instance.codigo_acceso:
        instance.codigo_acceso = generar_codigo_unico()

    if instance.pk:
        try:
            viejo = FormularioInscripcionHUT.objects.get(pk=instance.pk)
            # Guardamos temporalmente el grupo viejo en la instancia si ha cambiado
            if viejo.grupo != instance.grupo:
                instance._grupo_viejo = viejo.grupo
        except FormularioInscripcionHUT.DoesNotExist:
            pass

@receiver(post_save, sender=FormularioInscripcionHUT)
def actualizar_grupo_al_guardar(sender, instance, created, **kwargs):
    recalcular_participantes_grupo(instance.grupo)

    # Si cambió de grupo, recalculamos el viejo
    if hasattr(instance, '_grupo_viejo') and instance._grupo_viejo:
        recalcular_participantes_grupo(instance._grupo_viejo)

@receiver(post_delete, sender=FormularioInscripcionHUT)
def actualizar_grupo_al_eliminar(sender, instance, **kwargs):
    recalcular_participantes_grupo(instance.grupo)

