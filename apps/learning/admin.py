from django.contrib import admin
from .models import Badge, SkillPack, Module, Lesson, UserPackProgress

admin.site.register(Badge)
admin.site.register(SkillPack)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(UserPackProgress)
