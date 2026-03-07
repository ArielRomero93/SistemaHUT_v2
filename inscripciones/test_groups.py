from inscripciones.models import GruposMoodle, FormularioInscripcionHUT
def t():
    g1=GruposMoodle.objects.get(id=1)
    g2=GruposMoodle.objects.get(id=2)
    i=FormularioInscripcionHUT.objects.get(id=55)
    print("Initial - g1:", g1.participantes, "g2:", g2.participantes)
    
    i.grupo=g2
    i.save()
    g1.refresh_from_db()
    g2.refresh_from_db()
    print("After move to g2 - g1:", g1.participantes, "g2:", g2.participantes)
    
    i.grupo=g1
    i.save()
    g1.refresh_from_db()
    g2.refresh_from_db()
    print("After move back to g1 - g1:", g1.participantes, "g2:", g2.participantes)
t()
