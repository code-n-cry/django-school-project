from django.urls import path

import tasks.views

app_name = 'tasks'

urlpatterns = [
    path(
        '<int:team_id>/create/',
        tasks.views.TaskCreateView.as_view(),
        name='create',
    ),
    path('<int:pk>/done', tasks.views.TaskDoneView.as_view(), name='done'),
]
