from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json
import requests
from .forms import ProfileForm
from .models import Profile
from GoalShare.models import Follow, DailyReflection


def send_line_message(line_user_id, message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        'to': line_user_id,
        'messages': [{'type': 'text', 'text': message}],
    }
    requests.post(url, headers=headers, json=data)


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
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    if not profile.line_link_code:
        profile.generate_line_link_code()

    context = {
        'form': form,
        'line_link_code': profile.line_link_code,
    }
    return render(request, 'accounts/profile_edit.html', context)


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


@csrf_exempt
def line_webhook(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        events = json.loads(body).get('events', [])

        for event in events:
            if event.get('type') == 'message' and event['message'].get('type') == 'text':
                received_text = event['message']['text'].strip().upper()
                line_user_id = event['source']['userId']

                profile =