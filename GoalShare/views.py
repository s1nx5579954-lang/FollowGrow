from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import DailyReflection, Follow, Like
from .forms import DailyReflectionForm
from OneDay_todo.models import OneDayTask


@login_required
def reflection_create(request):
    today = timezone.localdate()

    existing = DailyReflection.objects.filter(user=request.user, date=today).first()

    completed_tasks = OneDayTask.objects.filter(
        one_day_list__user=request.user,
        is_completed=True,
        completed_at__date=today
    )
    task_names = '\n'.join(task.content for task in completed_tasks)

    if request.method == 'POST':
        if existing:
            form = DailyReflectionForm(request.POST, instance=existing)
        else:
            form = DailyReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.user = request.user
            reflection.date = today
            reflection.completed_tasks_snapshot = task_names
            reflection.save()
            return redirect('goalshare_timeline')
    else:
        form = DailyReflectionForm(instance=existing)

    context = {
        'form': form,
        'completed_tasks': completed_tasks,
        'existing': existing,
    }
    return render(request, 'goalshare/reflection_form.html', context)

@login_required
def timeline(request):
    following_ids = request.user.following.values_list('following_id', flat=True)

    my_tags = request.user.profile.tags.all()
    tag_matched_ids = User.objects.filter(
        profile__tags__in=my_tags
    ).exclude(id=request.user.id).values_list('id', flat=True)

    target_ids = set(list(following_ids) + list(tag_matched_ids) + [request.user.id])

    reflections = DailyReflection.objects.filter(
        user_id__in=target_ids
    ).select_related('user').prefetch_related('likes').distinct()

    liked_ids = set(request.user.likes.values_list('reflection_id', flat=True))

    context = {
        'reflections': reflections,
        'liked_ids': liked_ids,
    }
    return render(request, 'goalshare/timeline.html', context)
    
@login_required
def user_search(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

    following_ids = set(request.user.following.values_list('following_id', flat=True))

    context = {
        'query': query,
        'users': users,
        'following_ids': following_ids,
    }
    return render(request, 'goalshare/user_search.html', context)


@login_required
def follow_toggle(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST' and target_user != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )
        if not created:
            follow.delete()
    return redirect(request.META.get('HTTP_REFERER', 'goalshare_timeline'))


@login_required
def like_toggle(request, reflection_id):
    reflection = get_object_or_404(DailyReflection, id=reflection_id)
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, reflection=reflection)
        if not created:
            like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'goalshare_timeline'))
    