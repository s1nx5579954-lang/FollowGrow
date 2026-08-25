from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MonthlyList
from .forms import MonthlyListForm


@login_required
def index(request):
    lists = MonthlyList.objects.filter(user=request.user)
    list_form = MonthlyListForm()
    context = {
        'lists': lists,
        'list_form': list_form,
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


