# SistemaHUT_v2

Sistema de Inscripción HUT (Hasta lo Ultimo de la Tierra) — Django + SQLite + Tailwind CSS.

## Instalación

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# (Opcional) Cargar datos del JSON de respaldo
python manage.py loaddata /ruta/al/respaldodb.json

# Crear superusuario para el admin
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## Estructura del proyecto

```
SistemaHUT_v2/
├── config/            # Configuración Django
├── inscripciones/     # App principal
│   ├── models.py      # 8 tablas (Pais, Provincia, Inscripcion, etc.)
│   ├── views.py       # Lista + Formulario + API provincias
│   ├── forms.py       # ModelForm con Tailwind
│   └── templates/     # Templates con Tailwind CDN
├── manage.py
├── requirements.txt
└── db.sqlite3         # Base de datos SQLite
```
