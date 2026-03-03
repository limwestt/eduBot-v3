from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    LEVEL_CHOICES = [
        (1, 'Apprenti'),
        (2, 'Explorateur'),
        (3, 'Développeur'),
        (4, 'Expert'),
        (5, 'Maître'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)
    streak_days = models.PositiveIntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)
    badges = models.ManyToManyField('learning.Badge', blank=True)

    @property
    def xp_to_next_level(self):
        thresholds = {1: 500, 2: 1500, 3: 3500, 4: 7000, 5: 99999}
        return thresholds.get(self.level, 99999)

    @property
    def xp_percent(self):
        return min(int((self.xp / self.xp_to_next_level) * 100), 100)

    @property
    def level_display(self):
        return dict(self.LEVEL_CHOICES).get(self.level, 'Inconnu')

    def add_xp(self, amount: int):
        self.xp += amount
        while self.level < 5 and self.xp >= self.xp_to_next_level:
            self.level += 1
        self.save()

    def update_streak(self):
        """Appeler cette méthode à chaque action significative de l'utilisateur."""
        today = timezone.now().date()

        if self.last_activity is None:
            # Première activité
            self.streak_days = 1
            self.last_activity = today
            self.save()
            return

        delta = (today - self.last_activity).days

        if delta == 0:
            # Déjà actif aujourd'hui, rien à faire
            return
        elif delta == 1:
            # Actif hier → on continue la série
            self.streak_days += 1
            self.last_activity = today
            self.save()
        else:
            # Série brisée → on repart à 1
            self.streak_days = 1
            self.last_activity = today
            self.save()


class Notification(models.Model):
    TYPE_CHOICES = [
        ('xp',      ' XP gagné'),
        ('badge',   ' Badge obtenu'),
        ('mission', ' Mission complétée'),
        ('lesson',  ' Leçon complétée'),
        ('level',   ' Niveau atteint'),
        ('info',    ' Information'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    title      = models.CharField(max_length=100)
    message    = models.TextField(blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url        = models.CharField(max_length=200, blank=True)  # lien optionnel

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notif_type}] {self.user.username} — {self.title}"
