from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import *
from polls.forms import *


# Create your views here.

def index(request):
    polls = Poll.objects.all()
    return render(request, 'polls/index.html', {'polls': polls})


def create(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            return redirect('poll_details', pk=poll.pk)
    else:
        form = PollForm()

    return render(request, 'polls/create.html', {'form': form})


def edit(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == "POST":
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_details', pk=poll.pk)
    else:
        form = PollForm(instance=poll)


    return render(request, 'polls/edit.html', {'form': form})


def details(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    return render(request, 'polls/details.html', {'poll': poll})

def run(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == "POST":
        form = PollRunForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_details', pk=poll.pk)
    else:
        form = PollRunForm(instance=poll)
    return render(request, 'polls/run.html', {'form': form})


def delete(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.delete()
    return redirect('poll_index')
