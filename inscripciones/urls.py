from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscripcion_lista, name='inscripcion_lista'),
    path('formularioInscripcionHut/', views.inscripcion_crear, name='inscripcion_crear'),
    path('gracias/', views.inscripcion_gracias, name='inscripcion_gracias'),
    path('api/provincias/<int:pais_id>/', views.get_provincias, name='get_provincias'),
    path('exportar-moodle/', views.exportar_csv_moodle, name='exportar_csv_moodle'),
]
