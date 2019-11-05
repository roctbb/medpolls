from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import *
from polls.forms import *


# Create your views here.

def index(request):
    patients = Patient.objects.all()
    return render(request, 'patients/index.html', {'patients': patients})


def create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_details', pk=patient.pk)
    else:
        form = PatientForm()

    return render(request, 'patients/create.html', {'form': form})


def edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_details', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)


    return render(request, 'patients/edit.html', {'form': form})


def details(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    parameters = Parameter.objects.all()
    return render(request, 'patients/details.html', {'patient': patient, 'parameters': parameters})


def delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect('patient_index')
