import csv
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import FormularioInscripcionHUT, ProvinciaEstado, CursoHUT
from .forms import InscripcionForm
from .envio_mail import enviar_confirmacion_inscripcion


@login_required
def inscripcion_lista(request):
    """Vista principal: grilla de inscripciones (solo administradores logueados)."""
    query = request.GET.get('q', '').strip()
    inscripciones = FormularioInscripcionHUT.objects.select_related('pais', 'provincia').all()

    if query:
        inscripciones = inscripciones.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query) |
            Q(congregacion__icontains=query) |
            Q(ciudad__icontains=query) |
            Q(pastor__icontains=query)
        )

    paginator = Paginator(inscripciones, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'total': inscripciones.count(),
    }
    return render(request, 'inscripciones/lista.html', context)


def inscripcion_crear(request):
    """Formulario público para crear una nueva inscripción (sin login requerido)."""
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            enviar_confirmacion_inscripcion(inscripcion)
            return redirect('inscripcion_gracias')
    else:
        form = InscripcionForm()

    return render(request, 'publico/formulario_publico.html', {'form': form})


def inscripcion_gracias(request):
    """Página de agradecimiento post-inscripción (pública)."""
    return render(request, 'publico/gracias_publica.html')


def get_provincias(request, pais_id):
    """API JSON: devuelve provincias filtradas por país (para AJAX)."""
    provincias = ProvinciaEstado.objects.filter(idPais_id=pais_id).order_by('provinciaNombre')
    data = [{'id': p.id, 'nombre': p.provinciaNombre} for p in provincias]
    return JsonResponse(data, safe=False)



@login_required
def exportar_csv_moodle(request):
    """Exporta inscripciones del curso activo como XLSX compatible con Moodle."""
    import io
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    curso_activo = CursoHUT.objects.filter(activo=True).first()
    if not curso_activo:
        return HttpResponse("No hay curso activo.")

    inscripciones = (
        FormularioInscripcionHUT.objects
        .filter(curso=curso_activo)
        .order_by('apellido', 'nombre')
    )

    curso_nombre = curso_activo.nombre.replace(' ', '')
    fecha = datetime.now().strftime('%Y%m%d')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Moodle'

    # Estilos para el header
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='3D6B67', end_color='3D6B67', fill_type='solid')
    header_align = Alignment(horizontal='center')

    headers = ['username', 'firstname', 'lastname', 'email', 'course1', 'role1']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align

    # Datos
    for row, i in enumerate(inscripciones, 2):
        ws.cell(row=row, column=1, value=i.email)
        ws.cell(row=row, column=2, value=i.nombre)
        ws.cell(row=row, column=3, value=i.apellido)
        ws.cell(row=row, column=4, value=i.email)
        ws.cell(row=row, column=5, value=curso_nombre)
        ws.cell(row=row, column=6, value='student')

    # Auto-ancho de columnas
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    # Guardar en memoria
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    nombre_archivo = f'MOODLE_{curso_nombre}_{fecha}.xlsx'

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response