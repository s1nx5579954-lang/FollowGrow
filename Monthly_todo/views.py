import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MonthlyList
from .forms import MonthlyListForm
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from accounts.views import send_line_message
from django.views.decorators.csrf import csrf_exempt


@login_required
def index(request):
    lists = MonthlyList.objects.filter(user=request.user)
    list_form = MonthlyListForm()
    for l in lists:
        l.deadline_utc = l.deadline.astimezone(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
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


@login_required
def list_toggle(request, list_id):
    monthly_list = get_object_or_404(MonthlyList, id=list_id, user=request.user)
    if request.method == 'POST':
        monthly_list.is_completed = not monthly_list.is_completed
        monthly_list.save()

    return redirect('monthly_index')

@csrf_exempt
def check_deadlines(request):
    today = timezone.localdate()
    three_days_later = today + timezone.timedelta(days=3)
    one_day_later = today + timezone.timedelta(days=1)

    upcoming_lists = MonthlyList.objects.filter(
        is_completed=False
    ).select_related('user__profile')

    print(f"対象件数: {upcoming_lists.count()}件、今日: {today}、1日後: {one_day_later}、3日後: {three_days_later}")

    for l in upcoming_lists:
        deadline_local_date = timezone.localtime(l.deadline).date()
        print(f"チェック中: {l.title}, 締切日: {deadline_local_date}")

        if deadline_local_date not in [three_days_later, one_day_later]:
            continue

        line_user_id = l.user.profile.line_user_id
        if not line_user_id:
            print(f"{l.title}: line_user_idが未設定です")
            continue

        days_left = (deadline_local_date - today).days
        message = f"「{l.title}」の締め切りまで、あと{days_left}日です！"
        send_line_message(line_user_id, message)

    return HttpResponse('OK')

@login_required
def bulk_delete_completed(request):
    if request.method == 'POST':
        MonthlyList.objects.filter(
            user=request.user,
            is_completed=True
        ).delete()
    return redirect('monthly_index')


        
    