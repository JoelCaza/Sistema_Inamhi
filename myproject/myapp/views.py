# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel
from .forms import MyModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from io import BytesIO



# @login_required llama al login antes de que entre a el siguiente metodo
@login_required
def model_list(request): # vista del crud 
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})

def salir(request):
    logout(request)
    return redirect('/')

def model_detail(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_detail.html', {'model': model})


def model_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST)
        if form.is_valid():
            # Obtiene los datos del formulario
            cleaned_data = form.cleaned_data

            # Iterar sobre los campos y establecer "VACÍO" para los campos vacíos
            for field_name, field_value in cleaned_data.items():
                if not field_value: 
                    # Si el campo está vacío te muestra un mensaje de VACIO
                    cleaned_data[field_name] = 'VACÍO'

            # Crear una nueva instancia del formulario con los datos modificados
            form = MyModelForm(cleaned_data)

            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})




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


def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=model)
        if form.is_valid():
            # Redirige a la confirmación sin guardar los cambios
            request.session['form_data'] = form.cleaned_data
            return redirect('model_confirm_actualizar', pk=model.pk)
    else:
        form = MyModelForm(instance=model)
<<<<<<< Updated upstream
    return render(request, 'actualizar.html', {'form': form})

=======
    return render(request, 'actualizar.html', {'form': form, 'model': model})
    
>>>>>>> Stashed changes

def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})


def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        model.delete()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

#Exportacion de EXCEL
def export_to_excel(request):
    queryset = MyModel.objects.all()

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

#EXPORTA EL PDF
def export_to_pdf(request):
    queryset = MyModel.objects.all()

    # Crear un archivo PDF
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

    # Configurar estilos para el PDF
    styles = getSampleStyleSheet()

    # Tamaño de fuente relativo
    font_size = 10

    # Crear datos para la tabla en el PDF
    data = []
    column_names = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo',
                    'nombre_bien', 'serie', 'modelo', 'marca', 'color', 'material', 'estado',
                    'ubicacion', 'cedula', 'custodio_actual', 'observacion']
    data.append(column_names)
    for item in queryset:
        data.append([getattr(item, col) for col in column_names])

    # Calcular el ancho de la tabla en función del tamaño de la página
    page_width, page_height = pdf.pagesize
    available_width = page_width * 0.9  # Por ejemplo, el 90% del ancho de la página
    column_width = available_width / len(column_names)

    # Crear la tabla en el PDF
    table_data = []
    for row in data:
        table_row = []
        for item in row:
            adjusted_item = item[:50] + '...' if len(item) > 50 else item
            table_row.append(Paragraph(adjusted_item, styles['Normal']))
        table_data.append(table_row)

    table = Table(table_data, colWidths=[column_width] * len(column_names))

    # Configurar estilos para la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Construir el PDF
    pdf.build([table])

    # Obtener el contenido del PDF como un HttpResponse
    pdf_response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'attachment; filename=Reporte.pdf'

    return pdf_response