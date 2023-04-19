from django.urls import path

import tasks.views

app_name = 'tasks'

urlpatterns = [
    path(
        '<int:team_id>/create/',
        tasks.views.TaskCreateView.as_view(),
        name='create',
    ),
]
