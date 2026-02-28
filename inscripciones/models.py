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
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Grupo')
    curso = models.ForeignKey(CursoHUT, on_delete=models.PROTECT, verbose_name='Curso HUT')
    horario = models.CharField(max_length=100, verbose_name='Horario')
    dia = models.CharField(max_length=100, verbose_name='Día')
    tutor = models.CharField(max_length=100, verbose_name='Tutor')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

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
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área de Interés'
        verbose_name_plural = 'Áreas de Interés'


class Voluntario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    fecha_nacimiento = models.DateField()

    pais_origen = models.CharField(max_length=100)
    pais_residencia = models.CharField(max_length=100)
    provincia_residencia = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100)

    miembro_iglesia = models.CharField(max_length=10, choices=SI_NO)
    cual_iglesia = models.CharField(max_length=255, blank=True)

    sirve_en_iglesia = models.CharField(max_length=10, choices=SI_NO)
    cual_servicio = models.CharField(max_length=255, blank=True)

    tiempo_asistiendo = models.CharField(max_length=100, blank=True)

    voluntario_otra_org = models.CharField(max_length=10, choices=SI_NO)
    cual_org = models.CharField(max_length=255, blank=True)

    hizo_hut = models.CharField(max_length=20, choices=REALIZO_HUT)
    hizo_reacciona = models.CharField(max_length=20, choices=REALIZO_REACCIONA)

    deseo_salir_campo = models.CharField(max_length=30, choices=SI_NO_TALVEZ)

    nivel_estudio = models.CharField(max_length=30, choices=NIVEL_ESTUDIO)

    cursos_formacion = models.TextField(blank=True)
    experiencia_profesional = models.TextField(blank=True)

    areas_interes = models.ManyToManyField(AreaInteres, blank=True)

    foto_rostro = models.ImageField(
        upload_to='fotos_rostro/',
        validators=[validar_extension_imagen]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Voluntario'
        verbose_name_plural = 'Voluntarios'
