import re

with open('views.py', 'r') as f:
    content = f.read()

# Replace all `def form_valid(self, form):` with `def form_valid(self, form):\n        form.instance.usuario_auditoria = self.request.user`
content = re.sub(r'def form_valid\(self, form\):', r'def form_valid(self, form):\n        form.instance.usuario_auditoria = self.request.user', content)

with open('views.py', 'w') as f:
    f.write(content)
