from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lesson, SkillPack, UserPackProgress
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json



@login_required
def dashboard(request):
    skill_packs = SkillPack.objects.filter(is_published=True).order_by("order")
    
    # On enrichit chaque pack avec la progression de l'utilisateur
    packs_with_progress = []
    for pack in skill_packs:
        progress, _ = UserPackProgress.objects.get_or_create(
            user=request.user,
            pack=pack
        )
        packs_with_progress.append({
            'pack': pack,
            'progress': progress.progress_percent
        })
    
    stats = [
        {"label": "XP", "value": request.user.profile.xp},
        {"label": "Niveau", "value": request.user.profile.level_display},
        {"label": "Streak", "value": f"{request.user.profile.streak_days} Jours"},
        {"label": "Packs", "value": skill_packs.count()},
    ]
    
    return render(request, "learning/dashboard.html", {
        "packs_with_progress": packs_with_progress,
        "stats": stats,
        "daily_message": "Prêt pour ton défi IA du jour ?",
    })


@login_required
def pack_list(request):
    skill_packs = SkillPack.objects.filter(is_published=True).order_by("order")
    packs_with_progress = []
    for pack in skill_packs:
        progress, _ = UserPackProgress.objects.get_or_create(
            user=request.user, pack=pack
        )
        packs_with_progress.append({
            'pack': pack,
            'progress': progress.progress_percent
        })
    return render(request, "learning/pack_list.html", {
        "packs_with_progress": packs_with_progress
    })


@login_required
def pack_detail(request, slug):
    pack = get_object_or_404(SkillPack, slug=slug, is_published=True)
    modules = pack.modules.prefetch_related('lessons').all()
    progress, _ = UserPackProgress.objects.get_or_create(
        user=request.user, pack=pack
    )
    completed_lesson_ids = set(
        progress.completed_lessons.values_list('id', flat=True)
    )
    return render(request, "learning/pack_detail.html", {
        "pack": pack,
        "modules": modules,
        "progress": progress,
        "completed_lesson_ids": completed_lesson_ids,
    })


@login_required
def lesson_detail(request, pack_slug, lesson_id):
    pack = get_object_or_404(SkillPack, slug=pack_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__pack=pack)
    progress, _ = UserPackProgress.objects.get_or_create(
        user=request.user, pack=pack
    )
    already_completed = progress.completed_lessons.filter(id=lesson.id).exists()
    
    return render(request, "learning/lesson_detail.html", {
        "pack": pack,
        "lesson": lesson,
        "already_completed": already_completed,
    })


@login_required
@require_POST
def complete_lesson(request, pack_slug, lesson_id):
    pack = get_object_or_404(SkillPack, slug=pack_slug)
    from .models import Lesson
    lesson = get_object_or_404(Lesson, id=lesson_id, module__pack=pack)
    progress, _ = UserPackProgress.objects.get_or_create(
        user=request.user, pack=pack
    )

    already_done = progress.completed_lessons.filter(id=lesson.id).exists()

    if not already_done:
        progress.completed_lessons.add(lesson)
        request.user.profile.add_xp(lesson.xp_reward)
        request.user.profile.update_streak()   # <-- AJOUTER CETTE LIGNE
        return JsonResponse({
            "status": "ok",
            "xp_earned": lesson.xp_reward,
            "total_xp": request.user.profile.xp,
            "streak": request.user.profile.streak_days,   # <-- ET CELLE-CI
            "progress_percent": progress.progress_percent,
            "message": f"+{lesson.xp_reward} XP gagnés !"
        })

    return JsonResponse({"status": "already_done", "message": "Déjà complétée."})
