from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


# ── Profil utilisateur ──────────────────────────────────────────────

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# ── Notifications : Mission complétée ──────────────────────────────

def notify_mission_completed(sender, instance, created, **kwargs):
    from .models import Notification
    if instance.status == 'completed' and created:
        Notification.objects.create(
            user=instance.user,
            notif_type='mission',
            title='Mission accomplie ! 🎯',
            message=f'"{instance.mission.title}" — +{instance.xp_awarded} XP gagnés.',
            url=f'/missions/{instance.mission.id}/'
        )


# ── Notifications : Pack complété ──────────────────────────────────

def notify_pack_completed(sender, instance, **kwargs):
    from .models import Notification
    if instance.progress_percent == 100:
        already = Notification.objects.filter(
            user=instance.user,
            notif_type='xp',
            title__icontains=instance.pack.title
        ).exists()
        if not already:
            Notification.objects.create(
                user=instance.user,
                notif_type='xp',
                title='Pack terminé ! 🏆',
                message=f'Tu as complété le pack "{instance.pack.title}". Félicitations !',
                url=f'/packs/{instance.pack.slug}/'
            )


# ── Connexion des signaux ───────────────────────────────────────────

def connect_signals():
    from django.apps import apps

    UserMission     = apps.get_model('practice', 'UserMission')
    UserPackProgress = apps.get_model('learning', 'UserPackProgress')

    post_save.connect(notify_mission_completed, sender=UserMission)
    post_save.connect(notify_pack_completed,    sender=UserPackProgress)
