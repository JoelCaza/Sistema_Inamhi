# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel
from .forms import MyModelForm

def model_list(request):
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})

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
    return render(request, 'model_form.html', {'form': form})


def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        model.delete()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)



