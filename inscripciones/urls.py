from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscripcion_lista, name='inscripcion_lista'),
    path('formularioInscripcionHut/', views.inscripcion_crear, name='inscripcion_crear'),
    path('gracias/', views.inscripcion_gracias, name='inscripcion_gracias'),
    path('api/provincias/<int:pais_id>/', views.get_provincias, name='get_provincias'),
    path('exportar-moodle/', views.exportar_csv_moodle, name='exportar_csv_moodle'),

    # Grupos Moodle
    path('grupos/', views.GruposMoodleListView.as_view(), name='grupos_lista'),
    path('grupos/nuevo/', views.GruposMoodleCreateView.as_view(), name='grupos_crear'),
    path('grupos/editar/<int:pk>/', views.GruposMoodleUpdateView.as_view(), name='grupos_editar'),
    path('grupos/eliminar/<int:pk>/', views.GruposMoodleDeleteView.as_view(), name='grupos_eliminar'),
]
