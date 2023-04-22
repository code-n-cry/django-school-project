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
    django.urls.path(
        'yours/',
        teams.views.YoursTeamsView.as_view(),
        name='yours',
    ),
    django.urls.path(
        '<int:pk>/invite/',
        teams.views.TeamInviteUserView.as_view(),
        name='invite_user',
    ),
    django.urls.path(
        '<int:pk>/requests/',
        teams.views.TeamRequestsView.as_view(),
        name='requests',
    ),
    django.urls.path(
        '<int:pk>/members/',
        teams.views.TeamMembersView.as_view(),
        name='members',
    ),
    django.urls.path(
        '<int:team_pk>/members/<int:user_pk>/kick/',
        teams.views.TeamMemberKickView.as_view(),
        name='kick_member',
    ),
    django.urls.path(
        '<int:team_pk>/members/<int:user_pk>/give_lead/',
        teams.views.TeamMemberGiveLeadView.as_view(),
        name='give_lead_member',
    ),
    django.urls.path(
        '<int:team_id>/requests/<request_id>/accept',
        teams.views.RequestAcceptView.as_view(),
        name='request_accept',
    ),
    django.urls.path(
        '<int:team_id>/requests/<request_id>/reject',
        teams.views.RequestRejectView.as_view(),
        name='request_reject',
    ),
]
