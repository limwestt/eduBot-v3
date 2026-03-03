from django.urls import path
from .views import mission_list, mission_detail, submit_mission

app_name = 'practice'

urlpatterns = [
    path('missions/', mission_list, name='mission_list'),
    path('missions/<int:mission_id>/', mission_detail, name='mission_detail'),
    path('missions/<int:mission_id>/submit/', submit_mission, name='submit_mission'),
]
