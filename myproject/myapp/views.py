# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel
from .forms import MyModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages




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
            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})


def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm(instance=model)
        #ingreso del actualizar.html para que se llame al lugar de atudalizar
    return render(request, 'actualizar.html', {'form': form})
    #retorna a un html que preguntara si desea actualizar o no
    return redirect('model_confirm_actualizar.html', pk=pk)


def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})


def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        model.delete()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)



