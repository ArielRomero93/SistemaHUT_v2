from django.contrib import admin
from .models import (
    Usuario, OpcionesMenu, Pais, ProvinciaEstado,
    FormularioInscripcionHUT, FormularioDeDecision,
    AreaInteres, Voluntario
)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'paisNombre')
    search_fields = ('paisNombre',)


@admin.register(ProvinciaEstado)
class ProvinciaEstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'provinciaNombre', 'idPais')
    search_fields = ('provinciaNombre',)
    list_filter = ('idPais',)


@admin.register(FormularioInscripcionHUT)
class FormularioInscripcionHUTAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'pais', 'provincia', 'fecha_creacion', 'abandonado')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('pais', 'estadoCivil', 'abandonado', 'fecha_creacion')
    date_hierarchy = 'fecha_creacion'


@admin.register(FormularioDeDecision)
class FormularioDeDecisionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'servicioElegido', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('servicioElegido',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'ultimoIngreso')
    search_fields = ('username', 'email')
    list_filter = ('role',)


@admin.register(OpcionesMenu)
class OpcionesMenuAdmin(admin.ModelAdmin):
    list_display = ('Codigo', 'Descripcion', 'TipoOpcion')


@admin.register(AreaInteres)
class AreaInteresAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'pais_origen', 'hizo_hut')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('hizo_hut', 'deseo_salir_campo', 'nivel_estudio')
