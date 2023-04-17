import django.contrib.auth.decorators
import django.urls

import teams.views

app_name = 'teams'

urlpatterns = [
    django.urls.path(
        'create/',
        teams.views.CreateTeamView.as_view(),
        name='create',
    ),
    django.urls.path(
        '<int:pk>/',
        teams.views.TeamDetailView.as_view(),
        name='detail',
    ),
    django.urls.path(
        '',
        teams.views.TeamListView.as_view(),
        name='list',
    ),
    django.urls.path(
        '<int:pk>/edit/',
        teams.views.TeamEditView.as_view(),
        name='edit',
    ),
]
