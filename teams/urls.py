import django.contrib.auth.decorators
import django.urls

import teams.views

app_name = 'teams'

urlpatterns = [
    django.urls.path(
        'create/', teams.views.CreateTeamView.as_view(), name='create'
    ),
    django.urls.path(
        '<int:pk>/',
        teams.views.TeamDetailView.as_view(),
        name='team_detail',
    ),
    django.urls.path('list/', teams.views.TeamListView.as_view(), name='list'),
    django.urls.path('yours/', django.contrib.auth.decorators.login_required(
        teams.views.UsersTeamListView.as_view()
    ), name='yours'),
]
