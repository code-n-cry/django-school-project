from django.urls import path

import teams.views

app_name = 'teams'

urlpatterns = [
    path('create/', teams.views.CreateTeamView.as_view(), name='create'),
    path(
        '<int:pk>/',
        teams.views.TeamDetailView.as_view(),
        name='team_detail',
    ),
    path('list/', teams.views.TeamListView.as_view(), name='list'),
]
