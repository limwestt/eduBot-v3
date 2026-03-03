from django.db import models
from apps.accounts.models import User
from apps.learning.models import SkillPack


class Mission(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completée'),
        ('locked', 'Verrouillée'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    pack = models.ForeignKey(SkillPack, on_delete=models.SET_NULL, null=True, blank=True, related_name='missions')
    xp_reward = models.PositiveIntegerField(default=50)
    deadline = models.DateTimeField(null=True, blank=True)
    is_daily = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Mission.STATUS_CHOICES, default='active')
    submitted_answer = models.TextField(blank=True)
    ai_feedback = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    xp_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f"{self.user.username} — {self.mission.title} [{self.status}]"
