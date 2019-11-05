from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import *
from polls.forms import *


# Create your views here.

def index(request):
    rules = Rule.objects.all()
    return render(request, 'rules/index.html', {'rules': rules})


def create(request):
    if request.method == "POST":
        form = RuleForm(request.POST)
        if form.is_valid():
            rule = form.save()
            return redirect('rule_details', pk=rule.pk)
    else:
        form = RuleForm()

    return render(request, 'rules/create.html', {'form': form})


def edit(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == "POST":
        form = RuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('rule_details', pk=rule.pk)
    else:
        form = RuleForm(instance=rule)


    return render(request, 'rules/edit.html', {'form': form})


def details(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    return render(request, 'rules/details.html', {'rule': rule})


def delete(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    return redirect('rule_index')
