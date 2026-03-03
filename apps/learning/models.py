from django.db import models
from apps.accounts.models import User


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon_svg = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SkillPack(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    xp_reward = models.PositiveIntegerField(default=100)
    cover_image = models.ImageField(upload_to='packs/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Module(models.Model):
    pack = models.ForeignKey(SkillPack, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.pack.title} — {self.title}"


class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'Vidéo'),
        ('text', 'Article'),
        ('quiz', 'Quiz'),
        ('challenge', 'Défi pratique'),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    xp_reward = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class UserPackProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pack_progress')
    pack = models.ForeignKey(SkillPack, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def progress_percent(self):
        total = Lesson.objects.filter(module__pack=self.pack).count()
        if total == 0:
            return 0
        done = self.completed_lessons.count()
        return int((done / total) * 100)

    class Meta:
        unique_together = ('user', 'pack')

    def __str__(self):
        return f"{self.user.username} — {self.pack.title} ({self.progress_percent}%)"
