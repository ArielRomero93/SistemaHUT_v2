from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscripcion_lista, name='inscripcion_lista'),
    
    # --- INSCRIPCIONES ABIERTAS ---
    path('formularioInscripcionHut/', views.inscripcion_crear, name='inscripcion_crear'),

    # --- INSCRIPCIONES CERRADAS (Descomentar la línea de abajo y comentar la de arriba cuando cierren) ---
    #path('formularioInscripcionHut/', views.inscripciones_cerradas, name='inscripcion_crear'),
    
    path('gracias/', views.inscripcion_gracias, name='inscripcion_gracias'),
    path('api/provincias/<int:pais_id>/', views.get_provincias, name='get_provincias'),
    path('exportar-moodle/', views.exportar_csv_moodle, name='exportar_csv_moodle'),
    path('exportar-completo/', views.exportar_csv_completo, name='exportar_csv_completo'),

    # Cursos HUT (Admin)
    path('cursos/', views.CursoHUTListView.as_view(), name='cursos_lista'),
    path('cursos/nuevo/', views.CursoHUTCreateView.as_view(), name='cursos_crear'),
    path('cursos/editar/<int:pk>/', views.CursoHUTUpdateView.as_view(), name='cursos_editar'),
    path('cursos/eliminar/<int:pk>/', views.CursoHUTDeleteView.as_view(), name='cursos_eliminar'),

    # Grupos Moodle (Admin)
    path('grupos/', views.GruposMoodleListView.as_view(), name='grupos_lista'),
    path('grupos/nuevo/', views.GruposMoodleCreateView.as_view(), name='grupos_crear'),
    path('grupos/editar/<int:pk>/', views.GruposMoodleUpdateView.as_view(), name='grupos_editar'),
    path('grupos/eliminar/<int:pk>/', views.GruposMoodleDeleteView.as_view(), name='grupos_eliminar'),

    # Elección de Grupo Moodle (Público)
    path('mi-grupo/', views.inscripto_login_view, name='inscripto_login'),
    path('mi-grupo/seleccionar/', views.inscripto_seleccion_grupo_view, name='inscripto_seleccionar_grupo'),
    path('mi-grupo/exito/', views.inscripto_grupo_exito_view, name='inscripto_grupo_exito'),

    # Voluntarios (Público)
    path('aspirantes/', views.formulario_voluntario_crear, name='formulario_voluntario_crear'),
    path('aspirantes/gracias/', views.formulario_voluntario_gracias, name='formulario_voluntario_gracias'),

    # Importación de Alumnos (Admin)
    path('cambio-estado-alumno/', views.cambio_estado_alumno_view, name='cambio_estado_alumno'),
]
