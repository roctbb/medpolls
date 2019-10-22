from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import *
from polls.forms import *


# Create your views here.

def index(request):
    parameters = Parameter.objects.all()
    return render(request, 'parameters/index.html', {'parameters': parameters})


def create(request):
    if request.method == "POST":
        form = ParameterForm(request.POST)
        if form.is_valid():
            parameter = form.save()
            return redirect('parameter_details', pk=parameter.pk)
    else:
        form = ParameterForm()

    return render(request, 'parameters/create.html', {'form': form})


def edit(request, pk):
    parameter = get_object_or_404(Parameter, pk=pk)
    if request.method == "POST":
        form = ParameterForm(request.POST, instance=parameter)
        if form.is_valid():
            form.save()
            return redirect('parameter_details', pk=parameter.pk)
    else:
        form = ParameterForm(instance=parameter)


    return render(request, 'parameters/edit.html', {'form': form})


def details(request, pk):
    parameter = get_object_or_404(Parameter, pk=pk)
    return render(request, 'parameters/details.html', {'parameter': parameter})


def delete(request, pk):
    parameter = get_object_or_404(Parameter, pk=pk)
    parameter.delete()
    return redirect('parameter_index')
