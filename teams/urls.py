from django.urls import path

import teams.views

app_name = 'teams'

urlpatterns = [
    path(
        'create/',
        teams.views.CreateTeamView.as_view(),
        name='create',
    ),
    path(
        '<int:pk>/',
        teams.views.TeamDetailView.as_view(),
        name='detail',
    ),
    path(
        '',
        teams.views.TeamListView.as_view(),
        name='list',
    ),
    path(
        '<int:pk>/edit/',
        teams.views.TeamEditView.as_view(),
        name='edit',
    ),
]
