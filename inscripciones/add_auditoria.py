import re

with open('models.py', 'r') as f:
    content = f.read()

# Add the AuditoriaModel definition
if "class AuditoriaModel" not in content:
    replacement = """from django.db import models
from django.contrib.auth.models import User

class AuditoriaModel(models.Model):
    usuario_auditoria = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario Modificación")
    fecha_auditoria = models.DateTimeField(auto_now=True, verbose_name="Fecha Modificación")

    class Meta:
        abstract = True
"""
    content = content.replace("from django.db import models", replacement)

# Replace models.Model with AuditoriaModel for the targeted models
models_to_modify = [
    "Pais", "ProvinciaEstado", "CursoHUT", "Tutor", "GruposMoodle", 
    "FormularioInscripcionHUT", "FormularioDeDecision", "AreaInteres", 
    "Voluntario", "TerminosCondiciones"
]

for model_name in models_to_modify:
    pattern = rf"class {model_name}\(models\.Model\):"
    replacement = f"class {model_name}(AuditoriaModel):"
    content = re.sub(pattern, replacement, content)

with open('models.py', 'w') as f:
    f.write(content)
print("Updated models.py")
