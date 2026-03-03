from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from .models import Mission, UserMission
from apps.ai.services.groq_client import grade_mission


@login_required
def mission_list(request):
    daily_missions = Mission.objects.filter(is_daily=True)
    other_missions = Mission.objects.filter(is_daily=False)

    def enrich(missions):
        result = []
        for mission in missions:
            user_mission, _ = UserMission.objects.get_or_create(
                user=request.user,
                mission=mission,
                defaults={'status': 'active'}
            )
            result.append({'mission': mission, 'user_mission': user_mission})
        return result

    return render(request, 'practice/mission_list.html', {
        'daily_missions': enrich(daily_missions),
        'other_missions': enrich(other_missions),
    })


@login_required
def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    user_mission, _ = UserMission.objects.get_or_create(
        user=request.user,
        mission=mission,
        defaults={'status': 'active'}
    )

    return render(request, 'practice/mission_detail.html', {
        'mission':      mission,
        'user_mission': user_mission,
    })


@login_required
@require_POST
def submit_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    user_mission, _ = UserMission.objects.get_or_create(
        user=request.user,
        mission=mission,
        defaults={'status': 'active'}
    )

    # Déjà complétée
    if user_mission.status == 'completed':
        return JsonResponse({'status': 'already_done'})

    answer = request.POST.get('answer', '').strip()
    if not answer:
        return JsonResponse({'status': 'error', 'message': 'Réponse vide.'})

    # ── Appel IA ──────────────────────────────────────────
    try:
        ai_result = grade_mission(mission.description, answer)
    except Exception as e:
        return JsonResponse({
            'status':   'error',
            'message':  f'Erreur IA : {str(e)}'
        })

    passed       = ai_result.get('passed', False)
    score        = ai_result.get('score', 0)
    feedback     = ai_result.get('feedback', '')
    improvements = ai_result.get('improvements', [])

    # ── Mise à jour UserMission ───────────────────────────
    user_mission.submitted_answer = answer
    user_mission.completed_at     = timezone.now()

    if passed:
        user_mission.status     = 'completed'
        user_mission.xp_awarded = mission.xp_reward
        user_mission.save()

        # Créditer XP + streak
        request.user.profile.add_xp(mission.xp_reward)
        request.user.profile.update_streak()

        return JsonResponse({
            'status':       'ok',
            'passed':       True,
            'score':        score,
            'feedback':     feedback,
            'improvements': improvements,
            'xp_awarded':   mission.xp_reward,
            'total_xp':     request.user.profile.xp,
            'streak':       request.user.profile.streak_days,
            'message':      f'✅ Mission réussie ! +{mission.xp_reward} XP',
        })
    else:
        # Tentative échouée — on ne bloque pas, l'utilisateur peut réessayer
        user_mission.status = 'active'  # reste active pour permettre retry
        user_mission.save()

        return JsonResponse({
            'status':       'failed',
            'passed':       False,
            'score':        score,
            'feedback':     feedback,
            'improvements': improvements,
            'message':      f'Score : {score}/100 — Réessaie !',
        })
