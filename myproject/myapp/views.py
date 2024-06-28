# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel, CambioCustodio
from .forms import MyModelForm, CambioCustodioForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.db import migrations
from reportlab.lib.units import inch
import pytz


def home(request):
    return render(request, 'registration/login.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, '¡Usuario registrado correctamente!')
            return redirect('register')

    return render(request, 'registration/register.html', data)


#Permisos required
@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_detail(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_detail.html', {'model': model})

@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_list(request):
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            for field_name, field_value in instance._dict_.items():
                if not field_value and field_name != 'id':
                    setattr(instance, field_name, 'VACÍO')
            instance.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        cambio_form = CambioCustodioForm(request.POST)
        if form.is_valid() and cambio_form.is_valid():
            model = form.save(commit=False)
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
                model.save()

            cambio = model.cambiocustodio_set.first()
            if not cambio:
                cambio = CambioCustodio(modelo_relacionado=model)
            cambio.nuevo_custodio = cambio_form.cleaned_data['nuevo_custodio']
            cambio.cedula_nuevo_custodio = cambio_form.cleaned_data['cedula_nuevo_custodio']
            cambio.fecha_cambio = timezone.now()
            cambio.save()

            return redirect('model_list')
    else:
        form = MyModelForm(instance=model)
        cambio_form = CambioCustodioForm()

    return render(request, 'actualizar.html', {'form': form, 'cambio_custodio_form': cambio_form, 'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_confirm_actualizar(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form_data = request.session.get('form_data')
        if form_data:
            form = MyModelForm(form_data, instance=model)
            if form.is_valid():
                form.save()
                return redirect('model_list')
                
    else:
        form = MyModelForm(instance=model)
    return render(request, 'model_confirm_actualizar.html', {'form': form, 'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        model.estado_registro = False
        model.save()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

# @login_required llama al login antes de que entre a el siguiente metodo
@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')

@login_required
def salir(request):
    logout(request)
    return redirect('/')
@login_required
def model_detail(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_detail.html', {'model': model})
@login_required
def model_list(request):
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})
@login_required
def model_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            for field_name, field_value in instance._dict_.items():
                if not field_value and field_name != 'id':
                    setattr(instance, field_name, 'VACÍO')
            instance.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})
@login_required
def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        cambio_form = CambioCustodioForm(request.POST)
        if form.is_valid() and cambio_form.is_valid():
            model = form.save(commit=False)
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
                model.save()

            # Verificar si ya existe un objeto CambioCustodio para este modelo
            cambio = model.cambiocustodio_set.first()
            if not cambio:
                cambio = CambioCustodio(modelo_relacionado=model)
            cambio.nuevo_custodio = cambio_form.cleaned_data['nuevo_custodio']
            cambio.cedula_nuevo_custodio = cambio_form.cleaned_data['cedula_nuevo_custodio']
            cambio.fecha_cambio = timezone.now()  # Asigna la fecha actual
            cambio.save()

            return redirect('model_list')  # Redirigir a la lista de modelos después de la actualización
    else:
        form = MyModelForm(instance=model)
        cambio_form = CambioCustodioForm()

    return render(request, 'actualizar.html', {'form': form, 'cambio_custodio_form': cambio_form, 'model': model})


@login_required
def model_confirm_actualizar(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        # Guardar los cambios en la confirmación
        form_data = request.session.get('form_data')
        if form_data:
            form = MyModelForm(form_data, instance=model)
            if form.is_valid():
                form.save()
                return redirect('model_list')
                
    else:
        form = MyModelForm(instance=model)
    return render(request, 'model_confirm_actualizar.html', {'form': form, 'model': model})



@login_required
def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        # Cambiar el estado_registro a False y guardar el objeto
        model.estado_registro = False
        model.save()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

#Exportacion de EXCEL
def export_to_excel(request):
    queryset = MyModel.objects.filter(estado_registro=True)

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo',
                    'nombre_bien', 'serie', 'modelo', 'marca', 'color', 'material', 'estado',
                    'ubicacion', 'cedula', 'custodio_actual', 'observacion']
    ws.append(column_names)

    # Escribir datos
    for item in queryset:
        ws.append([getattr(item, col) for col in column_names])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)

    return response

def export_to_pdf(request):
    queryset = MyModel.objects.filter(estado_registro=True)

    # Crear un archivo PDF
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

    # Configurar estilos para el PDF
    styles = getSampleStyleSheet()
    # Añadir un nuevo estilo de párrafo con una fuente más pequeña (8 puntos) y un interlineado ajustado (10 puntos)
    styles.add(ParagraphStyle(name='TableStyle', fontSize=8, leading=10))
    font_size = 8  # Reducir el tamaño de la fuente para ajustarse mejor a las celdas

    # Añadir título y fecha de generación
    title = "Reporte de Bienes 2024"
    timezone_bogota = pytz.timezone('America/Bogota')
    fecha_generacion = f"Fecha de generación: {timezone.localtime(timezone.now(), timezone_bogota).strftime('%d-%m-%Y %H:%M:%S')}"


    title_paragraph = Paragraph(title, styles['Title'])
    date_paragraph = Paragraph(fecha_generacion, styles['Normal'])

    # Crear datos para la tabla en el PDF
    data = []
    column_names = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo',
                    'nombre_bien', 'serie', 'cedula', 'custodio_actual', 'archivo', 'nuevo_custodio', 'cedula_nuevo_custodio', 'fecha_cambio']
    data.append(column_names)

    # Obtener los valores de los campos para cada objeto en el queryset
    for item in queryset:
        row = []
        for col in column_names:
            value = getattr(item, col, None)
            if value is None:
                # Manejar campos relacionados (ForeignKey, OneToOneField)
                if hasattr(item, col):
                    related_obj = getattr(item, col)
                    value = str(related_obj)
                else:
                    value = 'N/A'
            elif isinstance(value, (str, int)):
                value = str(value)
            else:
                value = 'N/A'
            row.append(value)
        data.append(row)

    # Calcular el ancho de la tabla en función del tamaño de la página
    page_width, page_height = pdf.pagesize
    available_width = page_width * 0.95  # Usar el 95% del ancho de la página
    column_width = available_width / len(column_names)

    # Crear la tabla en el PDF
    table_data = []
    for row in data:
        table_row = []
        for item in row:
            # Ajustar el contenido de las celdas si es demasiado largo
            adjusted_item = item[:50] + '...' if len(item) > 50 else item
            table_row.append(Paragraph(adjusted_item, styles['TableStyle']))
        table_data.append(table_row)

    table = Table(table_data, colWidths=[column_width] * len(column_names))

    # Configurar estilos para la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Fondo gris para la fila de encabezado
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para la fila de encabezado
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear el texto a la izquierda
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la fila de encabezado
                        ('FONTSIZE', (0, 0), (-1, -1), font_size),  # Aplicar el tamaño de fuente reducido
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Relleno inferior para la fila de encabezado
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para las demás filas
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de cuadrícula negras
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinear el contenido de las celdas en la parte superior
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reducir el relleno izquierdo
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Reducir el relleno derecho
                        ('TOPPADDING', (0, 0), (-1, -1), 2)])  # Reducir el relleno superior
    table.setStyle(style)

    # Construir el PDF
    pdf.build([title_paragraph, Spacer(1, 0.2 * inch), date_paragraph, Spacer(1, 0.5 * inch), table])

    # Obtener el contenido del PDF como un HttpResponse
    pdf_response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'attachment; filename=Reporte.pdf'

    return pdf_response