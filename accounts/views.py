from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from GoalShare.models import Follow, DailyReflection
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def entrance(request):
    return render(request, 'accounts/entrance.html')

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)   # ← 修正
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    reflections = DailyReflection.objects.filter(user=target_user)

    is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()

    context = {
        'target_user': target_user,
        'reflections': reflections,
        'is_following': is_following,
        'following_count': target_user.following.count(),
        'followers_count': target_user.followers.count(),
        'is_own_profile': target_user == request.user,
    }
    return render(request, 'accounts/profile_view.html', context)