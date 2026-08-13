# oneday_todo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OneDayList, OneDayTask
from .forms import OneDayListForm, OneDayTaskForm


@login_required
def index(request):
    lists = OneDayList.objects.filter(user=request.user).prefetch_related('tasks')
    list_form = OneDayListForm()
    task_form = OneDayTaskForm()
    context = {
        'lists': lists,
        'list_form': list_form,
        'task_form': task_form,
    }
    return render(request, 'oneday_todo/index.html', context)


@login_required
def list_create(request):
    if request.method == 'POST':
        form = OneDayListForm(request.POST)
        if form.is_valid():
            one_day_list = form.save(commit=False)
            one_day_list.user = request.user
            one_day_list.save()
    return redirect('index')


@login_required
def task_add(request, list_id):
    one_day_list = get_object_or_404(OneDayList, id=list_id, user=request.user)
    if request.method == 'POST':
        form = OneDayTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.one_day_list = one_day_list
            task.save()
    return redirect('index')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(OneDayTask, id=task_id)
    if request.method == 'POST':
        task.delete()
    return redirect('index')


def task_toggle(request, task_id):
    task = get_object_or_404(OneDayTask, id=task_id)
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
    return redirect('index')

@login_required
def list_delete(request, list_id):
    one_day_list = get_object_or_404(OneDayList, id=list_id, user=request.user)
    if request.method == 'POST':
        one_day_list.delete()
    return redirect('index')