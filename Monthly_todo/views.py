from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MonthlyList, MonthlyTask
from .forms import MonthlyListForm, MonthlyTaskForm


@login_required
def index(request):
    lists = MonthlyList.objects.filter(user=request.user).prefetch_related('tasks')
    list_form = MonthlyListForm()
    task_form = MonthlyTaskForm()
    context = {
        'lists': lists,
        'list_form': list_form,
        'task_form': task_form,
    }
    return render(request, 'monthly_todo/index.html', context)


@login_required
def list_create(request):
    if request.method == 'POST':
        form = MonthlyListForm(request.POST)
        if form.is_valid():
            monthly_list = form.save(commit=False)
            monthly_list.user = request.user
            monthly_list.save()
    return redirect('monthly_index')


@login_required
def list_delete(request, list_id):
    monthly_list = get_object_or_404(MonthlyList, id=list_id, user=request.user)
    if request.method == 'POST':
        monthly_list.delete()
    return redirect('monthly_index')


@login_required
def task_add(request, list_id):
    monthly_list = get_object_or_404(MonthlyList, id=list_id, user=request.user)
    if request.method == 'POST':
        form = MonthlyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.monthly_list = monthly_list
            task.save()
    return redirect('monthly_index')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(MonthlyTask, id=task_id, monthly_list__user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('monthly_index')


@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(MonthlyTask, id=task_id, monthly_list__user=request.user)
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
    return redirect('monthly_index')