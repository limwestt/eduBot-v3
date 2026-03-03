from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from apps.learning.models import UserPackProgress
from apps.practice.models import UserMission


def register_view(request):
    if request.user.is_authenticated:
        return redirect('learning:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue sur EduBot, {user.username} !")
            return redirect('learning:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('learning:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('learning:dashboard')
        else:
            messages.error(request, "Identifiants incorrects. Réessaie.")
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile = request.user.profile

    # Packs en cours et complétés
    pack_progresses = UserPackProgress.objects.filter(
        user=request.user
    ).select_related('pack')

    completed_packs = [p for p in pack_progresses if p.progress_percent == 100]
    in_progress_packs = [p for p in pack_progresses if 0 < p.progress_percent < 100]

    # Missions complétées
    completed_missions = UserMission.objects.filter(
        user=request.user,
        status='completed'
    ).select_related('mission').order_by('-completed_at')

    # XP total gagné en missions
    total_mission_xp = sum(m.xp_awarded for m in completed_missions)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'completed_packs': completed_packs,
        'in_progress_packs': in_progress_packs,
        'completed_missions': completed_missions,
        'total_mission_xp': total_mission_xp,
        'badges': profile.badges.all(),
    })
