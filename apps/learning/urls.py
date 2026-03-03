from django.urls import path
from .views import dashboard, pack_list, pack_detail, lesson_detail, complete_lesson

app_name = "learning"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("packs/", pack_list, name="pack_list"),
    path("packs/<slug:slug>/", pack_detail, name="pack_detail"),
    path("packs/<slug:pack_slug>/lessons/<int:lesson_id>/", lesson_detail, name="lesson_detail"),
    path("packs/<slug:pack_slug>/lessons/<int:lesson_id>/complete/", complete_lesson, name="complete_lesson"),
]
